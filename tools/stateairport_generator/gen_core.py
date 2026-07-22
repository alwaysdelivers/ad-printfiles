from PIL import Image, ImageFont, ImageDraw
import numpy as np
FONT='/home/claude/gen/Monoton-Regular.ttf'
CANVAS=(3600,4800)
CODE_SIZE=1025   # fixed size, reproduces DFW exactly
# Code baseline anchor: from DFW real, code y[1337..2164]. DFW has no round overshoot top.
# We anchor by the code's baseline so overshoot extends UP consistently.
# DFW bottom (baseline area) ~ y2164. Use baseline_y = 2164.
CODE_BASELINE_Y = 2164

def render_fixed(txt, size, fill):
    f=ImageFont.truetype(FONT,size)
    tmp=Image.new('RGBA',(9000,5000),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    d.text((300,300),txt,font=f,fill=fill)
    a=np.array(tmp); al=a[:,:,3]; ys,xs=np.where(al>10)
    return tmp.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))

def render_ghost(txt, fill):
    # Rule B: fit natural bbox within 3000x1701
    base=1000; f=ImageFont.truetype(FONT,base)
    tmp=Image.new('RGBA',(9000,5000),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    d.text((300,300),txt,font=f,fill=fill); a=np.array(tmp)[:,:,3]; ys,xs=np.where(a>10)
    bw,bh=xs.max()-xs.min(),ys.max()-ys.min()
    s=min(3000/bw,1701/bh); size=int(round(base*s))
    f2=ImageFont.truetype(FONT,size); tmp2=Image.new('RGBA',(9000,6000),(0,0,0,0)); d2=ImageDraw.Draw(tmp2)
    d2.text((300,300),txt,font=f2,fill=fill); a2=np.array(tmp2)[:,:,3]; ys2,xs2=np.where(a2>10)
    return tmp2.crop((xs2.min(),ys2.min(),xs2.max()+1,ys2.max()+1))

def compose(ghost_txt, code_txt, ghost_rgb, code_rgb, ghost_alpha, lockup_img, lockup_xy):
    canvas=Image.new('RGBA',CANVAS,(0,0,0,0))
    # GHOST centered horizontally, top at y=900
    ghost=render_ghost(ghost_txt, ghost_rgb+(ghost_alpha,))
    gx=(CANVAS[0]-ghost.width)//2
    canvas.alpha_composite(ghost,(gx,900))
    # CODE fixed size, centered x, baseline-anchored (bottom at CODE_BASELINE_Y)
    code=render_fixed(code_txt, CODE_SIZE, code_rgb+(255,))
    cx=(CANVAS[0]-code.width)//2
    cy=CODE_BASELINE_Y-code.height
    canvas.alpha_composite(code,(cx,cy))
    # LOCKUP verbatim
    canvas.alpha_composite(lockup_img, lockup_xy)
    return canvas

if __name__=='__main__':
    lock=Image.open('/home/claude/gen/lockups/lockup_fc_light_tee.png').convert('RGBA')
    # reproduce DFW as gate
    dfw=compose('TX','DFW',(192,48,24),(30,58,95),127,lock,(706,3314))
    dfw.save('/home/claude/gen/repro_dfw2.png')
    lax=compose('CA','LAX',(192,48,24),(30,58,95),127,lock,(706,3314))
    lax.save('/home/claude/gen/lax2.png')
    print("built repro_dfw2 + lax2")
