from PIL import Image, ImageFont, ImageDraw
import numpy as np, math
FONT='/home/claude/gen/Monoton-Regular.ttf'
# canvases verified from real files
CANVAS={'tee':(3600,4800),'hoodie':(4200,4200)}
GHOST_TOP=900
GHOST_BOX=(3000,1701)          # RULE B per STATE_BUILD_PROTOCOL
HARMONY=2.0/3.0                # code target = state dims x 2/3
LOCK_XY={'tee':(706,3314),'hoodie':(1006,3314)}

def _render(txt,size,fill):
    f=ImageFont.truetype(FONT,size)
    tmp=Image.new('RGBA',(12000,7000),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    d.text((400,400),txt,font=f,fill=fill)
    a=np.array(tmp)[:,:,3]; ys,xs=np.where(a>10)
    return tmp.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))

def _nat(txt,base=1000):
    im=_render(txt,base,(0,0,0,255)); return im.width,im.height

def render_ghost(txt,fill):
    bw,bh=_nat(txt)
    s=min(GHOST_BOX[0]/bw, GHOST_BOX[1]/bh)      # RULE B
    return _render(txt,int(round(1000*s)),fill)

CAP_BASE=None
def _cap(base=1000):
    global CAP_BASE
    if CAP_BASE is None: CAP_BASE=_nat('H',base)[1]   # cap height: flat top/bottom, no curve overshoot
    return CAP_BASE

def render_code(code_txt,ghost_w,ghost_h,fill):
    # harmony-scale: target = state dims x 2/3 ; uniform scale = geometric mean.
    # Height uses CAP height (overshoot-corrected), per protocol's monoton overshoot correction.
    tw,th=ghost_w*HARMONY, ghost_h*HARMONY
    bw,_=_nat(code_txt)
    s=math.sqrt((tw/bw)*(th/_cap()))
    return _render(code_txt,int(round(1000*s)),fill)

def compose(ghost_txt, code_txt, ghost_rgb, code_rgb, ghost_alpha, lockup_img, lockup_xy, garment='tee'):
    W,H=CANVAS[garment]
    canvas=Image.new('RGBA',(W,H),(0,0,0,0))
    cx=W//2
    ghost=render_ghost(ghost_txt, ghost_rgb+(ghost_alpha,))
    canvas.alpha_composite(ghost,(cx-ghost.width//2, GHOST_TOP))
    gcy=GHOST_TOP+ghost.height//2
    code=render_code(code_txt, ghost.width, ghost.height, code_rgb+(255,))
    canvas.alpha_composite(code,(cx-code.width//2, gcy-code.height//2))   # centered on the state code
    canvas.alpha_composite(lockup_img, lockup_xy)
    return canvas
