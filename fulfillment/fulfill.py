import requests, json, re
RAW='https://raw.githubusercontent.com/alwaysdelivers/ad-printfiles/main/'
catalog=json.load(open('/home/claude/_catalog.json'))   # {'71':{'col|size':id}, '146':{...}}
norm=lambda s: re.sub(r'[^a-z0-9]','',(s or '').lower())
COLOR_ALIAS={'athheather':'athleticheather'}            # shopify token -> printful (normalized)
HOODIE_ALIAS={'athleticheather':'sportgrey'}            # Gildan 18500 names this grey differently than Bella 3001
LIGHT={'white','sand','ash','tan','athleticheather','natural','sportgrey','silver','babyblue','softcream','carolinablue','lightblue','heathercarolinablue'}  # use light(whitegarments) file
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
SCIENCE={
 'physics':  {'ar':1.133,'tee':(1150,260),'hoodie':(1300,200)},
 'geometry': {'ar':0.992,'tee':(1300,260),'hoodie':(1450,200)},
 'chemistry':{'ar':0.834,'tee':(1400,260),'hoodie':(1550,200)},
 'algebra':  {'ar':0.622,'tee':(1480,260),'hoodie':(1650,200)},
}
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
    if 'jesus' in t: return 'jesus'
    if 'karma' in t: return 'karma'
    for k in ('sasquatch','caveman','stork','yeti'):
        if k in t: return k
    if 'snowman' in t or 'abominable' in t: return 'snowman'
    if 'america' in t and '250' in t: return 'usa250'
    for k in ('physics','geometry','chemistry','algebra'):
        if k in t: return k
    return None
def line_to_item(title,color,size,qty=1,retail=None,print_style=None,ink=None):
    garment='hoodie' if 'hoodie' in title.lower() else 'tee'
    pid=146 if garment=='hoodie' else 71
    dk=design_of(title)
    if dk in SCIENCE:
        cw=(print_style or '').lower()                       # Colorway value, e.g. "White / Navy"
        gcol='black' if 'black' in cw else 'white'           # garment color drives the catalog blank
        ink=next((i for i in ('navy','oxblood','cream','sleet') if i in cw),'navy')
        cv=catalog[str(pid)].get('%s|%s'%(gcol,norm(size)))
        if not cv: return {'error':'UNFULFILLABLE (no Printful blank)','title':title,'colorway':print_style,'size':size}
        fp='printfiles/science/%s_%s.png'%(dk,ink)
        d=SCIENCE[dk]; aw,ah=AREA[garment]; w,top=d[garment]; h=int(w*d['ar']); left=(aw-w)//2
        return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':left}}],
                '_design':dk,'_garment':garment,'_file':fp,'_flags':[]}
    ckey=COLOR_ALIAS.get(norm(color),norm(color))
    if garment=='hoodie': ckey=HOODIE_ALIAS.get(ckey,ckey)
    cv=catalog[str(pid)].get('%s|%s'%(ckey,norm(size)))
    if not cv: return {'error':'UNFULFILLABLE (no Printful blank)','title':title,'color':color,'size':size}
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
    if dk=='yeti':
        ver=norm(print_style)
        code='YETI_drawing-ice_darkgarments.png' if ver in ('ice','iceblue','blue') else 'YETI_drawing_darkgarments.png'
        fp='printfiles/'+code
        aw,ah=AREA[garment]
        if garment=='hoodie': w,h,top=1637,2100,0        # MAX front (10.9" x 14")
        else: w,h,top=1600,int(1600/0.7796),110           # tee: validated on Men's 4
        return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':(aw-w)//2}}],
                '_design':'yeti','_garment':garment,'_file':fp,'_flags':[]}
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
