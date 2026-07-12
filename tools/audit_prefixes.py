#!/usr/bin/env python3
"""
AlwaysDelivers prefix consistency auditor.
Catches "GRANDMA drift": checks that every prefix's grid mockups are consistent across
the canonical source (ad-items) and both rendered surfaces (home, shop-all), that they
use baked heroes (not raw printfiles), and that every referenced image file exists.

Run after ANY prefix build/edit. Exit 0 = clean, exit 1 = drift found.
Usage: python3 audit_prefixes.py
"""
import json, subprocess, re, sys, urllib.request

THEME='153615171752'
def _tok(): return open('/tmp/_shoptoken').read().strip()
def _pat(): return open('/tmp/_ghpat').read().strip()

def fetch_asset(key):
    r=subprocess.run(['curl','-s','-G',
        f'https://rudjph-mx.myshopify.com/admin/api/2025-07/themes/{THEME}/assets.json',
        '--data-urlencode',f'asset[key]={key}','-H',f'X-Shopify-Access-Token: {_tok()}'],
        capture_output=True,text=True).stdout
    d=json.loads(r)
    return d['asset']['value'] if 'asset' in d else None

def parse_ad_items(v):
    i=v.find('[{"name"'); depth=0; j=i; instr=False; esc=False
    while j<len(v):
        ch=v[j]
        if esc:esc=False
        elif ch=='\\':esc=True
        elif ch=='"':instr=not instr
        elif not instr:
            if ch=='[':depth+=1
            elif ch==']':
                depth-=1
                if depth==0:break
        j+=1
    return json.loads(v[i:j+1])

def card_imgs(html, id_prefix):
    """Extract per-product-url list of swatch data-img from a rendered section."""
    out={}
    # match each tile: href="/products/..." ... <div class="...-sws">(swatches)</div>
    for m in re.finditer(r'href="(/products/[^"]+)".*?class="[a-z0-9-]*sws">(.*?)</div>', html, re.S):
        url=m.group(1); sws=m.group(2)
        imgs=re.findall(r'data-img="([^"]+)"', sws)
        if imgs: out[url]=imgs
    return out

def repo_hero_set():
    r=urllib.request.Request(f'https://api.github.com/repos/alwaysdelivers/ad-printfiles/contents/heroes/grid',
        headers={'Authorization':'Bearer '+_pat(),'User-Agent':'AlwaysDelivers'})
    return set(f['name'] for f in json.loads(urllib.request.urlopen(r).read()))

def base(u): return u.split('/')[-1].rsplit('.',1)[0]

def main():
    ai=fetch_asset('snippets/ad-items.liquid')
    home=fetch_asset('sections/home.liquid')
    sa=fetch_asset('sections/shop-all.liquid')
    if not all([ai,home,sa]):
        print('ERROR: could not fetch one of ad-items/home/shop-all'); return 1
    AD=parse_ad_items(ai)
    home_cards=card_imgs(home,'h2')
    sa_cards=card_imgs(sa,'sa2')
    repo=repo_hero_set()

    problems=[]
    print(f'{"PREFIX":18} {"SRC TYPE":13} {"HOME":10} {"SHOP-ALL":10} {"FILES EXIST":12}')
    print('-'*70)
    for c in AD:
        name=c['name']; url=c['tee_url']
        canon=[col['tee'] for col in c['colors']]
        # (a) source type
        src='baked' if all('heroes/grid' in u for u in canon) else 'RAW/MIXED'
        if src!='baked': problems.append(f'{name}: canonical uses non-baked images ({src})')
        # (b) home + shop-all match canonical (image identity, by base name)
        cb=[base(u) for u in canon]
        h=home_cards.get(url); s=sa_cards.get(url)
        home_st='n/a' if h is None else ('ok' if [base(x) for x in h]==cb else 'DRIFT')
        sa_st='MISSING' if s is None else ('ok' if [base(x) for x in s]==cb else 'DRIFT')
        if home_st=='DRIFT': problems.append(f'{name}: home diverges from ad-items')
        if sa_st in ('DRIFT','MISSING'): problems.append(f'{name}: shop-all {sa_st.lower()}')
        # (c) files exist in repo
        missing=[u.split("/")[-1] for u in canon if 'heroes/grid' in u and u.split("/")[-1] not in repo]
        files_st='ok' if not missing else f'MISSING {len(missing)}'
        if missing: problems.append(f'{name}: {len(missing)} hero files missing from repo: {missing[:2]}')
        print(f'{name:18} {src:13} {home_st:10} {sa_st:10} {files_st:12}')
    print()
    if problems:
        print(f'❌ {len(problems)} PROBLEM(S) FOUND:')
        for p in problems: print('  -',p)
        return 1
    print('✅ ALL PREFIXES CONSISTENT — no drift.')
    return 0

if __name__=='__main__':
    sys.exit(main())
