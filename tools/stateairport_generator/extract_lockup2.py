# Extract verbatim lockups for ALL 4 tokens x 2 garments, using per-token alpha threshold
from PIL import Image
import numpy as np, urllib.request, io, os
RAW='https://raw.githubusercontent.com/alwaysdelivers/ad-printfiles/main/printfiles/stateairport/'
def load(p): return Image.open(io.BytesIO(urllib.request.urlopen(RAW+p,timeout=30).read())).convert('RGBA')
os.makedirs('/home/claude/gen/lockups',exist_ok=True)
tokens=['fc_light','redstate_white','neonstate_white','goldstate_white']
for tok in tokens:
    for gar in ['tee','hoodie']:
        fn=f'STATEAIRPORT_tx-dfw_{tok}_{gar}_r2.png'
        im=load(fn); a=np.array(im); al=a[:,:,3]
        # lockup zone below y3200 (well below any code). Use low threshold to catch 75% too.
        solid=(al>=40).copy(); solid[:3200,:]=False
        ys,xs=np.where(solid)
        pad=8
        box=(max(0,xs.min()-pad),max(0,ys.min()-pad),min(a.shape[1],xs.max()+pad),min(a.shape[0],ys.max()+pad))
        crop=im.crop(box)
        crop.save(f'/home/claude/gen/lockups/lockup_{tok}_{gar}.png')
        # also record the exact top-left placement for recompositing
        print(f"{tok} {gar}: {crop.size} placed at x={box[0]} y={box[1]} (alpha_max={al[solid].max()})")
