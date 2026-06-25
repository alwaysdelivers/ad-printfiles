import requests, json, re
RAW='https://raw.githubusercontent.com/alwaysdelivers/ad-printfiles/main/'
catalog=json.load(open('/home/claude/_catalog.json'))   # {'71':{'col|size':id}, '146':{...}}
norm=lambda s: re.sub(r'[^a-z0-9]','',(s or '').lower())
COLOR_ALIAS={'athheather':'athleticheather'}            # shopify token -> printful (normalized)
HOODIE_ALIAS={'athleticheather':'sportgrey'}            # Gildan 18500 names this grey differently than Bella 3001
LIGHT={'white','sand','ash','tan','athleticheather','natural','sportgrey','silver','babyblue','babypink','softcream','carolinablue','lightblue','heathercarolinablue'}  # use light(whitegarments) file
SLATEC={'silver','ash','softcream','sand'}
WARM={'maroon','oxbloodblack','olive','militarygreen','forestgreen','heatheremerald'}
def _mono_ink(ckey):
    if ckey=='red': return 'charcoal'
    if ckey in SLATEC: return 'slate'
    if ckey in LIGHT: return 'navy'
    if ckey in WARM: return 'gold'
    return 'cream'
AREA={'tee':(1800,2400),'hoodie':(2100,2100)}
MOCKUP_MODEL={'tee':"Men's 4",'hoodie':"Men's 4"}  # canonical Printful option_group for ALL listing mockups
DESIGNS={
 'sasquatch':{'light':'printfiles/SASQUATCH_sqt-01_whitegarments.png','dark':'printfiles/SASQUATCH_sqt-01_darkgarments.png','ar':0.671,'hoodie':(1680,420),'tee':(1600,500)},
 'caveman':{'light':'printfiles/CAVEMAN_cav-08_whitegarments.png','dark':'printfiles/CAVEMAN_cav-08_darkgarments.png','ar':0.681,'hoodie':(1680,420),'tee':(1600,500)},
 'snowman':{'light':'printfiles/SNOWMAN_snw-01_whitegarments.png','dark':'printfiles/SNOWMAN_snw-01_darkgarments.png','ar':0.755,'hoodie':(1500,420),'tee':(1400,500)},
 'stork':{'light':'printfiles/STORK_stk-07_whitegarments.png','dark':'printfiles/STORK_stk-07_darkgarments.png','ar':0.468,'hoodie':(1500,560),'tee':(1450,620)},
 'yeti':{'light':None,'dark':'printfiles/YETI_drawing_darkgarments.png','ar':1.283,'hoodie':(1150,250),'tee':(1350,440)},
 'usa250':{'light':'printfiles/AMERICA250_usa-250_whitegarments.png','dark':'printfiles/AMERICA250_usa-250_darkgarments.png','special':{'red':'printfiles/AMERICA250_usa-250_REDcharcoal.png'},'ar':0.687,'hoodie':(1600,440),'tee':(1500,500)},
}
# JESUS = one product, Style axis selects the lettering treatment. Trimmed art, top-anchored in a box (matches v2 mockups).
JESUS_STYLES={'serif':('jes-01',1.349),'script':('jes-03',1.071),'bold':('jes-07',1.249),'retro':('jes-11',1.461)}  # style -> (file code, aspect w/h)
JESUS_BOX={'tee':(1250,1100,480),'hoodie':(1250,1100,470)}  # maxw, maxh, top
# SCIENCE = one product per prefix, Colorway option = "{Garment} / {Ink}". 4 mono inks; placement locked: tee top 260 / hoodie top 200.
SCIENCE={                       # combined Science product; Design option picks subject; ink by ground; full-width-contain, top-anchored.
 'physics':1.133,'geometry':0.992,'chemistry':0.834,'algebra':0.622,   # ar = printfile H/W (3600-wide frameless)
}
SCIENCE_TOP={'tee':260,'hoodie':200}
# FAITH = same frame standard as JESUS (4500x5400, y1350 top-anchor, gap 420). Style -> (file code, aspect w/h).
FAITH_STYLES={'classic':('faith-01',1.915),'elegant':('faith-02',1.867),'strong':('faith-04',1.349)}
# placements validated this session: all hoodies + KARMA tee. TEE creature/Stork tops are best-fit estimates -> spot-check.
# KARMA = one product per garment; Design option = spiral+lockup variant. Per-color print files (4500x5400, Printful auto-fits).
KARMA_FILES={                                   # norm(Design value) -> file (fixed regardless of ground)
 'bluetealblue':'KARMA_blueteal_sblue.png','bluetealteal':'KARMA_blueteal_steal.png',
 'allblueblue':'KARMA_allblue_kblue.png','allbluenavy':'KARMA_allblue_navy.png',
 'blackbluenavy':'KARMA_blackblue_navy.png','redwhitecream':'KARMA_redwhite_cream.png',
 'redwhitered':'KARMA_redwhite_bred.png','bluewhitecream':'KARMA_bluewhite_cream.png',
 'bluewhiteblue':'KARMA_bluewhite_kblue.png','slatewhitecream':'KARMA_slatewhite_cream.png'}
KARMA_BBBLUE={'light':'KARMA_blackblue_sblue.png','dark':'KARMA_blackblue_blueonly_sblue.png'}  # Black/Blue·Blue swaps art by ground
KARMA_AR=4500/5400                              # print-file aspect (w/h); Printful auto-fits the full file
UNVERIFIED_TEE=set()  # all verified on Men's 4 model
def design_of(title):
    t=title.lower()
    if 'crown' in t: return 'crown'
    if 'jesus' in t: return 'jesus'
    if 'faith' in t: return 'faith'
    if 'karma' in t: return 'karma'
    if 'creature' in t: return 'creatures'      # combined Creatures product: route by Design option
    for k in ('sasquatch','caveman','stork','yeti'):
        if k in t: return k
    if 'snowman' in t or 'abominable' in t: return 'snowman'
    if 'america' in t and '250' in t: return 'usa250'
    if 'science' in t: return 'science'
    return None
def line_to_item(title,color,size,qty=1,retail=None,print_style=None,ink=None):
    garment='hoodie' if 'hoodie' in title.lower() else 'tee'
    pid=146 if garment=='hoodie' else 71
    dk=design_of(title)
    if dk=='science':                                        # combined Science: Design option (option3) picks subject
        design=norm(print_style)
        if design not in SCIENCE:
            return {'error':'SCIENCE missing/invalid Design option','title':title,'design':print_style,'color':color,'size':size}
        ckey=COLOR_ALIAS.get(norm(color),norm(color))
        if garment=='hoodie': ckey=HOODIE_ALIAS.get(ckey,ckey)
        cv=catalog[str(pid)].get('%s|%s'%(ckey,norm(size)))
        if not cv: return {'error':'UNFULFILLABLE (no Printful blank)','title':title,'color':color,'size':size}
        ink='navy' if ckey in LIGHT else 'cream'             # single ink by ground (navy on light, cream on dark)
        fp='printfiles/science/%s_%s.png'%(design,ink)
        aw,ah=AREA[garment]; ar=SCIENCE[design]              # full-width-contain, top-anchored
        w=aw; h=w*ar
        if h>ah: h=ah; w=h/ar
        left=(aw-w)/2; ta=SCIENCE_TOP[garment]; top=max(0,min(ta,ah-h))
        return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':round(w),'height':round(h),'top':round(top),'left':round(left)}}],
                '_design':'science-'+design,'_garment':garment,'_file':fp,'_flags':[]}
    ckey=COLOR_ALIAS.get(norm(color),norm(color))
    if garment=='hoodie': ckey=HOODIE_ALIAS.get(ckey,ckey)
    cv=catalog[str(pid)].get('%s|%s'%(ckey,norm(size)))
    if not cv: return {'error':'UNFULFILLABLE (no Printful blank)','title':title,'color':color,'size':size}
    if dk=='crown':
        # CROWN: Ink property = Full Color (split file, light grounds only) or Mono (single-color file).
        # Files are full 4500x5400 frame -> auto-fit, aspect-preserved & centered (like Karma).
        CK={'white':'White','athleticheather':'Heather','sportgrey':'Heather','navy':'Navy','black':'Black'}
        cc=CK.get(ckey)
        if not cc: return {'error':'CROWN unknown color','title':title,'color':color,'size':size}
        inkv=(ink or '').strip().lower()
        light=ckey in LIGHT
        if inkv in ('full color','fullcolor','fc') and light:
            fp='printfiles/crown/%s_split.png'%cc.lower()
        else:
            fp='printfiles/crown/%s.png'%cc.lower()      # Mono / single-color; dark grounds always single
        CROWN_AR=4500.0/5400.0
        aw,ah=AREA[garment]
        if aw/ah<=CROWN_AR: w=aw; h=int(aw/CROWN_AR)
        else: h=ah; w=int(ah*CROWN_AR)
        top=(ah-h)//2; left=(aw-w)//2
        return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':left}}],
                '_design':'crown','_garment':garment,'_file':fp,'_flags':[]}
    if dk=='karma':
        key=norm(print_style)
        if key=='blackblueblue':
            fp=KARMA_BBBLUE['light' if ckey in LIGHT else 'dark']      # Black/Blue·Blue: b+b art on light, blue-only on dark
        elif key in KARMA_FILES:
            fp=KARMA_FILES[key]
        else:
            return {'error':'KARMA missing/invalid Design option','title':title,'design':print_style,'color':color,'size':size}
        aw,ah=AREA[garment]
        if aw/ah<=KARMA_AR: w=aw; h=int(aw/KARMA_AR)                   # full-file auto-fit, aspect-preserved & centered
        else: h=ah; w=int(ah*KARMA_AR)
        top=(ah-h)//2; left=(aw-w)//2
        return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':left}}],
                '_design':'karma','_garment':garment,'_file':fp,'_flags':[]}
    if dk=='jesus':
        st=norm(print_style)
        if st not in JESUS_STYLES: return {'error':'JESUS missing/invalid Style option','title':title,'color':color,'size':size}
        code,aspect=JESUS_STYLES[st]
        t=(ink or '').strip().lower()
        if t=='red' and ckey!='navy':
            fp='printfiles/jesus/%s_redmono.png'%code              # all-red, single ink (red not offered on navy)
        else:
            ground='light' if ckey in LIGHT else 'dark'
            if t=='mono': ground+='_mono'
            fp='printfiles/jesus/%s_%s.png'%(code,ground)
        aw,ah=AREA[garment]; maxw,maxh,top=JESUS_BOX[garment]
        if aspect>=maxw/maxh: w=maxw; h=int(maxw/aspect)
        else: h=maxh; w=int(maxh*aspect)
        left=(aw-w)//2
        return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':left}}],
                '_design':'jesus','_garment':garment,'_file':fp,'_flags':[]}
    if dk=='faith':
        st=norm(print_style)
        if st not in FAITH_STYLES: return {'error':'FAITH missing/invalid Style option','title':title,'color':color,'size':size}
        code,aspect=FAITH_STYLES[st]
        t=(ink or '').strip().lower()
        if t=='red' and ckey!='navy':
            fp='printfiles/faith/%s_redmono.png'%code
        else:
            ground='light' if ckey in LIGHT else 'dark'
            if t=='mono': ground+='_mono'
            fp='printfiles/faith/%s_%s.png'%(code,ground)
        aw,ah=AREA[garment]; maxw,maxh,top=JESUS_BOX[garment]
        if aspect>=maxw/maxh: w=maxw; h=int(maxw/aspect)
        else: h=maxh; w=int(maxh*aspect)
        left=(aw-w)//2
        return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':left}}],
                '_design':'faith','_garment':garment,'_file':fp,'_flags':[]}
    if dk=='yeti':
        ver=norm(print_style)
        ice=ver in ('ice','iceblue','blue')
        base=('YETI_drawing-ice_darkgarments' if ice
              else ('YETI_drawing_whitegarments' if ckey in LIGHT else 'YETI_drawing_darkgarments'))
        # hoodie uses dropped-placement files (head lowered, ~12% smaller); tee uses originals
        code=base+('_hoodie.png' if garment=='hoodie' else '.png')
        fp='printfiles/'+code
        aw,ah=AREA[garment]
        if garment=='hoodie': w,h,top=1637,2100,0        # MAX front (Printful auto-fits the file)
        else: w,h,top=1600,int(1600/0.7796),110           # tee: validated on Men's 4
        return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':(aw-w)//2}}],
                '_design':'yeti','_garment':garment,'_file':fp,'_flags':[]}
    if dk=='creatures':                                  # combined Creatures: Design option picks the creature
        cr=norm(print_style)
        if cr in ('yeti','yetiiceblue','yetiice','iceblue'):
            ice = cr!='yeti'
            base=('YETI_drawing-ice_darkgarments' if ice
                  else ('YETI_drawing_whitegarments' if ckey in LIGHT else 'YETI_drawing_darkgarments'))
            code=base+('_hoodie.png' if garment=='hoodie' else '.png')   # yeti hoodie uses dropped-placement files
            fp='printfiles/'+code; aw,ah=AREA[garment]
            w,h,top=(1637,2100,0) if garment=='hoodie' else (1600,int(1600/0.7796),110)
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':(aw-w)//2}}],
                    '_design':'creatures','_garment':garment,'_file':fp,'_flags':[]}
        dk={'caveman':'caveman','sasquatch':'sasquatch','abominablesnowman':'snowman','snowman':'snowman','abominable':'snowman'}.get(cr)
        if not dk: return {'error':'CREATURES unknown design','title':title,'design':print_style,'color':color,'size':size}
        # text creatures fall through to the DESIGNS handler below (ground-aware light/dark + their own placement)
    d=DESIGNS[dk]
    fp=d['light'] if (ckey in LIGHT and d['light']) else d['dark']
    if d.get('special') and ckey in d['special']: fp=d['special'][ckey]
    if dk=='usa250' and (print_style or '').strip().lower()=='mono': fp='printfiles/AMERICA250_usa-250_MONO_%s.png'%_mono_ink(ckey)
    aw,ah=AREA[garment]; w,top=d[garment]; h=int(w*d['ar']); left=(aw-w)//2
    flags=[]
    if garment=='tee' and dk in UNVERIFIED_TEE: flags.append('TEE_PLACEMENT_UNVERIFIED')
    return {'variant_id':cv,'quantity':qty,'retail_price':retail,
            'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':left}}],
            '_design':dk,'_garment':garment,'_file':fp,'_flags':flags}
