#!/usr/bin/env python3
"""
AlwaysDelivers CMYK-gamut audit gate.
Catches colors that can't be reproduced on coated CMYK and will shift on press
(Printful's "color shift" warning). Soft-proofs every significant solid color
through FOGRA39 (coated) and reports the shift as CIE76 dE.
  dE < 4  OK   |   4-6  WARN (minor shift)   |   > 6  FAIL (out of gamut)
Run:  python3 tools/audit_gamut.py [dir_or_files ...]   (default: printfiles + KARMA_*.png)
Exit 1 if anything FAILS.
"""
import sys, os, glob
import numpy as np
from PIL import Image, ImageCms
HERE=os.path.dirname(os.path.abspath(__file__))
SRGB=ImageCms.getOpenProfile(os.path.join(HERE,'icc','sRGB.icc'))
CMYK=ImageCms.getOpenProfile(os.path.join(HERE,'icc','FOGRA39L_coated.icc'))
RI=ImageCms.Intent.RELATIVE_COLORIMETRIC
TC=ImageCms.buildTransform(SRGB,CMYK,'RGB','CMYK',renderingIntent=RI)
TB=ImageCms.buildTransform(CMYK,SRGB,'CMYK','RGB',renderingIntent=RI)
def proof(c):
    im=Image.new('RGB',(1,1),tuple(int(x) for x in c))
    return list(ImageCms.applyTransform(ImageCms.applyTransform(im,TC),TB).getpixel((0,0)))
def s2lab(c):
    r,g,b=[v/255 for v in c]; lin=lambda u:((u+0.055)/1.055)**2.4 if u>0.04045 else u/12.92
    r,g,b=lin(r),lin(g),lin(b)
    X=(r*.4124+g*.3576+b*.1805)/.95047;Y=r*.2126+g*.7152+b*.0722;Z=(r*.0193+g*.1192+b*.9505)/1.08883
    f=lambda t:t**(1/3) if t>.008856 else 7.787*t+16/116
    return (116*f(Y)-16,500*(f(X)-f(Y)),200*(f(Y)-f(Z)))
def dE(a,b): return sum((x-y)**2 for x,y in zip(s2lab(a),s2lab(b)))**0.5
def hx(c): return '#%02x%02x%02x'%tuple(int(x) for x in c)
def audit(path):
    im=np.asarray(Image.open(path).convert('RGBA')); rgb=im[:,:,:3]; al=im[:,:,3]
    vis=rgb[al>200]
    if len(vis)==0: return path,'PASS',[]
    cols,cnts=np.unique(vis.reshape(-1,3),axis=0,return_counts=True)
    flags=[]
    for c,n in zip(cols,cnts):
        share=n/len(vis)
        if share<0.02: continue
        d=dE(list(c),proof(list(c)))
        if d>=4: flags.append((hx(c),hx(proof(list(c))),round(d,1),round(share*100)))
    flags.sort(key=lambda x:-x[2])
    worst=max([f[2] for f in flags],default=0)
    v='FAIL' if worst>6 else ('WARN' if worst>=4 else 'PASS')
    return path,v,flags
args=sys.argv[1:] or ['printfiles','KARMA_*.png']
files=[]
for x in args: files += glob.glob(os.path.join(x,'*.png')) if os.path.isdir(x) else glob.glob(x)
files=sorted(set(files)); bad=0
for p in files:
    _,v,flags=audit(p)
    if v=='FAIL': bad+=1
    if v!='PASS':
        det=' '.join('%s->%s dE%.0f(%d%%)'%(a,b,d,s) for a,b,d,s in flags)
        print('%-5s %-34s %s'%(v,os.path.basename(p),det))
print('\n%d files · %d FAIL (out of gamut) · gate %s'%(len(files),bad,'BLOCK' if bad else 'clear'))
sys.exit(1 if bad else 0)
