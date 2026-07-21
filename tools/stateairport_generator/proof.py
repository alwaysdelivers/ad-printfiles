# Compare my repro to the real tx-dfw, build a visual side-by-side + diff metrics
from PIL import Image
import numpy as np, urllib.request, io, base64
RAW='https://raw.githubusercontent.com/alwaysdelivers/ad-printfiles/main/printfiles/stateairport/'
real=Image.open(io.BytesIO(urllib.request.urlopen(RAW+'STATEAIRPORT_tx-dfw_fc_light_tee_r2.png',timeout=30).read())).convert('RGBA')
repro=Image.open('/home/claude/gen/repro_dfw.png').convert('RGBA')
ra=np.array(real); pa=np.array(repro)
# metrics on alpha coverage
def bbox(a):
    ys,xs=np.where(a[:,:,3]>10); return xs.min(),xs.max(),ys.min(),ys.max()
print("real bbox:",bbox(ra))
print("repro bbox:",bbox(pa))
# composite both on white, thumbnail side by side
def onwhite(im):
    bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
rw=onwhite(real); pw=onwhite(repro)
def b64(im,mw=380):
    im=im.copy(); im.thumbnail((mw,mw)); buf=io.BytesIO(); im.save(buf,'PNG'); return base64.b64encode(buf.getvalue()).decode()
html=f'''<!doctype html><html><head><meta charset="utf-8"><title>DFW repro proof</title>
<style>body{{font-family:sans-serif;background:#eee;padding:20px;text-align:center}}
.row{{display:flex;gap:20px;justify-content:center}}.col{{background:#fff;padding:14px;border-radius:12px}}
img{{max-width:100%}}h3{{margin:6px}}</style></head><body>
<h2>§8 Proof Gate: reproduce tx-dfw before building CA</h2>
<div class="row">
<div class="col"><h3>REAL tx-dfw (shipped)</h3><img src="data:image/png;base64,{b64(rw)}"></div>
<div class="col"><h3>MY REPRO (generator)</h3><img src="data:image/png;base64,{b64(pw)}"></div>
</div>
<p>If these match, the generator is trustworthy for CA (swap TX→CA ghost, DFW→LAX/etc code).</p>
</body></html>'''
open('/mnt/user-data/outputs/dfw_repro_proof.html','w').write(html)
print("built proof")
