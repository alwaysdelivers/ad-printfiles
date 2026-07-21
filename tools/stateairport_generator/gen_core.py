from PIL import Image, ImageFont, ImageDraw
import numpy as np
FONT='/home/claude/gen/Monoton-Regular.ttf'
CANVAS=(3600,4800)

def render_monoton(txt, target_w=None, target_h=None, fill=(0,0,0,255)):
    """Render text in Monoton, scaled so its tight bbox hits target_w or target_h (whichever binds)."""
    # render at a base size, measure, then scale
    base=1000
    f=ImageFont.truetype(FONT,base)
    tmp=Image.new('RGBA',(8000,4000),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    d.text((200,200),txt,font=f,fill=fill)
    a=np.array(tmp); al=a[:,:,3]; ys,xs=np.where(al>10)
    bw,bh=xs.max()-xs.min(),ys.max()-ys.min()
    # scale factor
    if target_w and target_h:
        s=min(target_w/bw, target_h/bh)
    elif target_w: s=target_w/bw
    else: s=target_h/bh
    size=int(round(base*s))
    f2=ImageFont.truetype(FONT,size)
    tmp2=Image.new('RGBA',(9000,5000),(0,0,0,0)); d2=ImageDraw.Draw(tmp2)
    d2.text((300,300),txt,font=f2,fill=fill)
    a2=np.array(tmp2); al2=a2[:,:,3]; ys2,xs2=np.where(al2>10)
    crop=tmp2.crop((xs2.min(),ys2.min(),xs2.max()+1,ys2.max()+1))
    return crop

def compose(ghost_txt, code_txt, ghost_rgb, code_rgb, ghost_alpha, lockup_img, lockup_xy,
            code_box, ghost_rule='B'):
    """Compose one airport print file."""
    canvas=Image.new('RGBA',CANVAS,(0,0,0,0))
    # GHOST: Rule B -> fit within 3000 x 1701, centered. Natural aspect of the 2-letter code.
    ghost=render_monoton(ghost_txt, target_w=3000, target_h=1701, fill=ghost_rgb+(ghost_alpha,))
    # if width-bound gave <3000 but height <1701, that's fine; place centered horizontally, 
    # vertically centered on the design block center (measured from ref)
    gx=(CANVAS[0]-ghost.width)//2
    # ghost vertical center: from ref, TX ghost spanned y[900..~2900]; its visual center ~ 1900? 
    # Measured: ghost bbox y start 900. We'll place ghost top at y=900 (protocol: block top 900).
    gy=900
    canvas.alpha_composite(ghost,(gx,gy))
    # CODE: fit to measured code box (w=2730 h=827 for DFW). Center at cx=1799, cy from box.
    cw=code_box[2]-code_box[0]; ch=code_box[3]-code_box[1]
    code=render_monoton(code_txt, target_w=cw, target_h=ch, fill=code_rgb+(255,))
    cx=(CANVAS[0]-code.width)//2
    cy=code_box[1]
    canvas.alpha_composite(code,(cx,cy))
    # LOCKUP: paste verbatim at recorded xy
    canvas.alpha_composite(lockup_img, lockup_xy)
    return canvas

if __name__=='__main__':
    # PROOF: reproduce tx-dfw fc_light tee
    lock=Image.open('/home/claude/gen/lockups/lockup_fc_light_tee.png').convert('RGBA')
    out=compose('TX','DFW', ghost_rgb=(192,48,24), code_rgb=(30,58,95), ghost_alpha=127,
                lockup_img=lock, lockup_xy=(706,3314),
                code_box=(434,1337,3164,2164))
    out.save('/home/claude/gen/repro_dfw.png')
    print("saved repro_dfw.png", out.size)
