# Fully decompose tx-dfw to derive EVERY parameter: canvas, ghost box, code box, lockup box, colors, opacity
from PIL import Image
import numpy as np, urllib.request, io
RAW='https://raw.githubusercontent.com/alwaysdelivers/ad-printfiles/main/printfiles/stateairport/'
def load(p): return np.array(Image.open(io.BytesIO(urllib.request.urlopen(RAW+p,timeout=30).read())).convert('RGBA'))
dfw=load('STATEAIRPORT_tx-dfw_fc_light_tee_r2.png')
aus=load('STATEAIRPORT_tx-aus_fc_light_tee_r2.png')
H,W=dfw.shape[:2]; print("canvas",W,H)
al=dfw[:,:,3]
# 1. LOCKUP: shared between dfw/aus AND in lower zone. Isolate solid pixels y>2300
same=(np.abs(dfw.astype(int)-aus.astype(int)).sum(axis=2)<12)
lock=(al>=250)&same; lock[:2300,:]=False
ly,lx=np.where(lock)
print("LOCKUP: x[%d..%d] y[%d..%d] w=%d h=%d cx=%d"%(lx.min(),lx.max(),ly.min(),ly.max(),lx.max()-lx.min(),ly.max()-ly.min(),(lx.min()+lx.max())//2))
# 2. CODE: solid, differs between dfw/aus, upper zone
code=(al>=250)&(~same); code[2300:,:]=False
cy,cx=np.where(code)
print("CODE(DFW): x[%d..%d] y[%d..%d] w=%d h=%d cx=%d"%(cx.min(),cx.max(),cy.min(),cy.max(),cx.max()-cx.min(),cy.max()-cy.min(),(cx.min()+cx.max())//2))
# 3. GHOST: faint ~127 everywhere (it's behind both code and extends). Full bbox:
ghost=(al>=120)&(al<=134)
gy,gx=np.where(ghost)
print("GHOST(TX) full: x[%d..%d] y[%d..%d] w=%d h=%d cx=%d"%(gx.min(),gx.max(),gy.min(),gy.max(),gx.max()-gx.min(),gy.max()-gy.min(),(gx.min()+gx.max())//2))
# ghost color + exact opacity
gcol=dfw[ghost]; print("ghost RGB mean:",int(gcol[:,0].mean()),int(gcol[:,1].mean()),int(gcol[:,2].mean()),"alpha mean:",int(gcol[:,3].mean()))
ccol=dfw[code]; print("code  RGB mean:",int(ccol[:,0].mean()),int(ccol[:,1].mean()),int(ccol[:,2].mean()))
# Rule B check: ghost fits 3000x1701 box. natural TX aspect -> which binds?
