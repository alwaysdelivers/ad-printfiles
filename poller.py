#!/usr/bin/env python3
"""
AlwaysDelivers fulfillment poller.

Runs on a 5-minute schedule via GitHub Actions. Each run:
  1. Mints a fresh Shopify Admin API token (client_credentials grant).
  2. Pulls PAID + UNFULFILLED Shopify orders.
  3. Skips any order already recorded in _processed.json.
  4. Translates each line via fulfill.line_to_item -> Printful order items.
  5. Creates ONE Printful order per Shopify order
     (DRAFT unless CONFIRM_ORDERS=true, in which case it is submitted for production).
  6. Records the outcome in _processed.json (the workflow commits it back to the repo).

Idempotency = two independent guards:
  - the committed state file _processed.json (primary), and
  - Printful external_id = Shopify order id (backstop, survives a lost state file).

This build does INTAKE only (Shopify order -> Printful order).
It does NOT yet write shipping/tracking back to Shopify -- that's a separate later step.
fulfill.py is imported and used as-is; nothing in it is modified.
"""
import os, sys, json, time, pathlib, requests

HERE = pathlib.Path(__file__).resolve().parent
STATE_PATH = HERE / "_processed.json"
sys.path.insert(0, str(HERE))   # so `import fulfill` finds fulfillment/fulfill.py

# --- config from env (GitHub Actions secrets/variables) ----------------------
SHOP           = os.environ["SHOPIFY_SHOP"]            # e.g. rudjph-mx.myshopify.com
SHOP_CLIENT_ID = os.environ["SHOPIFY_CLIENT_ID"]
SHOP_SECRET    = os.environ["SHOPIFY_CLIENT_SECRET"]
PF_TOKEN       = os.environ["PRINTFUL_TOKEN"]
PF_STORE_ID    = os.environ["PRINTFUL_STORE_ID"]
CONFIRM        = os.environ.get("CONFIRM_ORDERS", "false").strip().lower() == "true"
API_VER        = os.environ.get("SHOPIFY_API_VERSION", "2025-01")
GQL_URL        = f"https://{SHOP}/admin/api/{API_VER}/graphql.json"

import fulfill  # noqa: E402  (after env so a missing catalog fails loudly in the CI seed step)

TERMINAL = {"created", "duplicate", "unfulfillable"}  # never reprocess these

ORDERS_Q = """
query($cursor:String){
  orders(first:25, after:$cursor, sortKey:CREATED_AT,
         query:"financial_status:paid AND fulfillment_status:unfulfilled"){
    pageInfo{ hasNextPage endCursor }
    edges{ node{
      id legacyResourceId name email createdAt
      shippingAddress{ name address1 address2 city provinceCode countryCodeV2 zip phone }
      lineItems(first:50){ edges{ node{
        title quantity
        originalUnitPriceSet{ shopMoney{ amount } }
        variant{ title selectedOptions{ name value } }
      }}}
    }}
  }
}"""


def shopify_token():
    r = requests.post(f"https://{SHOP}/admin/oauth/access_token",
                      json={"client_id": SHOP_CLIENT_ID, "client_secret": SHOP_SECRET,
                            "grant_type": "client_credentials"}, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def gql(token, query, variables=None):
    r = requests.post(GQL_URL,
                      headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
                      json={"query": query, "variables": variables or {}}, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError("Shopify GraphQL errors: %s" % json.dumps(data["errors"]))
    return data["data"]


def line_opts(node):
    var = node.get("variant") or {}
    opts = {o["name"].lower(): o["value"] for o in (var.get("selectedOptions") or [])}
    return opts.get("color"), opts.get("size")


def build_items(node):
    """Returns (items, errors). One Printful item per Shopify line."""
    items, errors = [], []
    for e in node["lineItems"]["edges"]:
        li = e["node"]
        color, size = line_opts(li)
        price = (li.get("originalUnitPriceSet") or {}).get("shopMoney", {}).get("amount")
        item = fulfill.line_to_item(li["title"], color, size, li["quantity"], price)
        if item.get("error"):
            errors.append(f"{li['title']} / {color} / {size}: {item['error']}")
        else:
            items.append({k: v for k, v in item.items() if not k.startswith("_")})
    return items, errors


def recipient(node):
    a = node.get("shippingAddress") or {}
    return {
        "name":         a.get("name") or node.get("name") or "",
        "address1":     a.get("address1") or "",
        "address2":     a.get("address2") or "",
        "city":         a.get("city") or "",
        "state_code":   a.get("provinceCode") or "",
        "country_code": a.get("countryCodeV2") or "",
        "zip":          a.get("zip") or "",
        "phone":        a.get("phone") or "",
        "email":        node.get("email") or "",
    }


def create_printful(external_id, recip, items):
    url = "https://api.printful.com/orders" + ("?confirm=1" if CONFIRM else "")
    body = {"external_id": str(external_id), "recipient": recip, "items": items}
    r = requests.post(url,
                      headers={"Authorization": f"Bearer {PF_TOKEN}",
                               "X-PF-Store-Id": str(PF_STORE_ID),
                               "Content-Type": "application/json"},
                      json=body, timeout=60)
    if r.status_code in (200, 201):
        return "created", (r.json().get("result") or {}).get("id")
    # An order with this external_id already exists -> we made it on a prior run.
    txt = r.text.lower()
    if r.status_code in (400, 409) and ("exist" in txt or "already" in txt or "duplicate" in txt):
        return "duplicate", None
    raise RuntimeError(f"Printful {r.status_code}: {r.text[:600]}")


def load_state():
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text() or "{}")
        except Exception:
            return {}
    return {}


def save_state(st):
    STATE_PATH.write_text(json.dumps(st, indent=2, sort_keys=True))


def main():
    st = load_state()
    token = shopify_token()
    created = errored = skipped = 0
    cursor = None
    while True:
        conn = gql(token, ORDERS_Q, {"cursor": cursor})["orders"]
        for edge in conn["edges"]:
            node = edge["node"]
            oid, name = str(node["legacyResourceId"]), node["name"]
            if st.get(oid, {}).get("status") in TERMINAL:
                skipped += 1
                continue
            items, errs = build_items(node)
            if errs:
                print(f"ERROR  {name} ({oid}) UNFULFILLABLE: " + "; ".join(errs))
                st[oid] = {"status": "unfulfillable", "detail": errs, "name": name, "ts": int(time.time())}
                errored += 1
                continue
            if not items:
                print(f"SKIP   {name} ({oid}) no recognizable design lines")
                skipped += 1
                continue
            try:
                status, pf_id = create_printful(oid, recipient(node), items)
            except Exception as ex:
                # transient -> do NOT record, so it retries next run
                print(f"RETRY  {name} ({oid}) Printful error, will retry next run: {ex}")
                continue
            mode = "CONFIRMED/production" if CONFIRM else "DRAFT"
            print(f"OK     {name} ({oid}) -> Printful {status} id={pf_id} [{mode}] items={len(items)}")
            st[oid] = {"status": status, "printful_id": pf_id, "confirmed": CONFIRM,
                       "name": name, "ts": int(time.time())}
            created += 1
        if conn["pageInfo"]["hasNextPage"]:
            cursor = conn["pageInfo"]["endCursor"]
            continue
        break

    save_state(st)
    print(f"\nSUMMARY  created/duplicate={created}  unfulfillable={errored}  "
          f"skipped(already done / unrecognized)={skipped}  confirm_mode={CONFIRM}")
    if errored:
        print("::warning::Some orders were UNFULFILLABLE - see ERROR lines above.")


if __name__ == "__main__":
    main()
