#!/usr/bin/env python3
"""
AlwaysDelivers print-file audit gate.
Catches the #1 production defect: a non-transparent background, faint matte, or halo
that prints as a visible rectangular box on dark garments.

Print files are tight-cropped to the art, so canvas-edge tests don't apply. The
reliable, illustration-safe signals are:
  - no alpha channel                          -> opaque background, guaranteed box
  - coverage of the bbox > 90%                -> the whole rectangle is inked = a box
  - a faint semi-transparent plateau          -> a matte/underlay (invisible on screen,
    (most-common nonzero alpha < 200 covering    prints as film). Clean art's most-common
     >8% of canvas, OR >12% of canvas              nonzero alpha is 255 (solid ink) and
     sits at alpha 1..127)                         only ~2-5% is anti-aliasing.

Run:  python3 tools/audit_printfiles.py [dir_or_files ...]   (default: printfiles + KARMA_*.png)
Exit 1 if anything FAILS.
"""
import sys, os, glob
import numpy as np
from PIL import Image
INK=6
def audit(path):
    im=Image.open(path)
    if not ((im.mode in ('RGBA','LA')) or ('transparency' in im.info)):
        return dict(f=os.path.basename(path),v='FAIL',cov='-',mnz='-',faint='-',r='NO ALPHA (opaque background)')
    a=np.asarray(im.convert('RGBA'))[:,:,3].astype(int); tot=a.size
    ink=a>=INK
    if not ink.any():
        return dict(f=os.path.basename(path),v='FAIL',cov='-',mnz='-',faint='-',r='empty / nothing prints')
    ys,xs=np.where(ink); cov=ink[ys.min():ys.max()+1, xs.min():xs.max()+1].mean()
    nz=a[a>0]; vals,cnts=np.unique(nz,return_counts=True); i=cnts.argmax()
    mnz_val=int(vals[i]); mnz_share=cnts[i]/tot
    faint=((a>=1)&(a<128)).sum()/tot
    v,r='PASS','clean: transparent ground, art-shaped ink'
    if cov>0.90:
        v,r='FAIL','SOLID BOX: %.0f%% of bbox is inked (rectangle, not art)'%(cov*100)
    elif mnz_val<200 and mnz_share>0.08:
        v,r='FAIL','MATTE: %.0f%% of canvas at uniform alpha %d (semi-transparent box)'%(mnz_share*100,mnz_val)
    elif faint>0.12:
        v,r='FAIL','HALO/MATTE: %.0f%% of canvas semi-transparent (should be ~2-5%% AA)'%(faint*100)
    elif cov>0.80:
        v,r='WARN','dense: %.0f%% bbox coverage — eyeball it'%(cov*100)
    return dict(f=os.path.basename(path),v=v,cov='%.0f%%'%(cov*100),
                mnz='%d/%.0f%%'%(mnz_val,mnz_share*100),faint='%.0f%%'%(faint*100),r=r)

args=sys.argv[1:]
files=[]
if not args: args=['printfiles','KARMA_*.png']
for x in args:
    files += glob.glob(os.path.join(x,'*.png')) if os.path.isdir(x) else glob.glob(x)
files=sorted(set(files))
rows=[audit(f) for f in files]; w=max(len(r['f']) for r in rows); bad=0
print('%-*s  %-5s  cov   most-nz   faint  reason'%(w,'FILE','OK'))
print('-'*(w+62))
for r in rows:
    if r['v']!='PASS': bad+=1
    print('%-*s  %-5s  %-4s  %-8s  %-5s  %s'%(w,r['f'],r['v'],r['cov'],r['mnz'],r['faint'],r['r']))
print('\n%d files audited · %d need attention'%(len(rows),bad))
sys.exit(1 if bad else 0)
