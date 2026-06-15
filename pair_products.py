#!/usr/bin/env python3
"""
AlwaysDelivers — auto-pair each Tee <-> Hoodie via the custom.paired_product metafield.
Idempotent: safe to run on a schedule. Only writes pairs that are missing/wrong.

Matching:
  - group = the product's `design:<id>` tag if present, else its normalized title
  - garment = productType ("T-Shirt"/"Tee" -> tee, "Hoodie" -> hoodie)
  Any group that has BOTH a tee and a hoodie gets linked both directions.

Auth (reuse your fulfill-poller secrets):
  SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET   (mints a token via client_credentials)
  or SHOPIFY_TOKEN
"""
import os, re, sys, json, urllib.request

SHOP = os.environ.get("SHOP", "rudjph-mx.myshopify.com")
API  = "2025-07"
NS, KEY = "custom", "paired_product"

def _post(url, data, headers):
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def get_token():
    if os.environ.get("SHOPIFY_TOKEN"):
        return os.environ["SHOPIFY_TOKEN"]
    cid, sec = os.environ.get("SHOPIFY_CLIENT_ID"), os.environ.get("SHOPIFY_CLIENT_SECRET")
    if not (cid and sec):
        sys.exit("Set SHOPIFY_TOKEN, or SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET.")
    o = _post(f"https://{SHOP}/admin/oauth/access_token",
              {"client_id": cid, "client_secret": sec, "grant_type": "client_credentials"},
              {"Content-Type": "application/json"})
    if "access_token" not in o:
        sys.exit(f"Token mint failed: {o}")
    return o["access_token"]

def gql(tok, q, v=None):
    o = _post(f"https://{SHOP}/admin/api/{API}/graphql.json",
              {"query": q, "variables": v or {}},
              {"Content-Type": "application/json", "X-Shopify-Access-Token": tok})
    if "errors" in o:
        sys.exit(f"GraphQL error: {o['errors']}")
    return o["data"]

QUERY = """query($c:String){
  products(first:100, after:$c){
    pageInfo{ hasNextPage endCursor }
    nodes{ id title productType tags
      paired: metafield(namespace:"%s", key:"%s"){ value } } } }""" % (NS, KEY)

def garment(pt, title):
    s = (pt + " " + title).lower()
    if "hoodie" in s: return "hoodie"
    if "shirt" in s or "tee" in s: return "tee"
    return None

def group_key(p):
    for t in p["tags"]:
        if t.startswith("design:"):
            return t
    s = p["title"].lower()
    for w in ["always delivers", "premium", "hoodie", "tee", "t-shirt", "—", "-", "|"]:
        s = s.replace(w, " ")
    return re.sub(r"[^a-z0-9]+", "", s)

def main():
    tok = get_token()
    prods, cursor = [], None
    while True:
        d = gql(tok, QUERY, {"c": cursor})["products"]
        prods += d["nodes"]
        if not d["pageInfo"]["hasNextPage"]:
            break
        cursor = d["pageInfo"]["endCursor"]

    groups = {}
    for p in prods:
        g = garment(p["productType"], p["title"])
        if g:
            groups.setdefault(group_key(p), {})[g] = p

    inputs = []
    for gd in groups.values():
        if "tee" in gd and "hoodie" in gd:
            tee, hood = gd["tee"], gd["hoodie"]
            if (tee.get("paired") or {}).get("value") != hood["id"]:
                inputs.append({"ownerId": tee["id"], "namespace": NS, "key": KEY,
                               "type": "product_reference", "value": hood["id"]})
            if (hood.get("paired") or {}).get("value") != tee["id"]:
                inputs.append({"ownerId": hood["id"], "namespace": NS, "key": KEY,
                               "type": "product_reference", "value": tee["id"]})

    if not inputs:
        print("All tee/hoodie pairs already linked — nothing to do.")
        return

    M = """mutation($mf:[MetafieldsSetInput!]!){
      metafieldsSet(metafields:$mf){ userErrors{ field message } } }"""
    for i in range(0, len(inputs), 25):
        res = gql(tok, M, {"mf": inputs[i:i+25]})["metafieldsSet"]
        if res["userErrors"]:
            print("ERRORS:", res["userErrors"])
    print(f"Linked/updated {len(inputs)} metafields ({len(inputs)//2} new/changed pairs).")

if __name__ == "__main__":
    main()
