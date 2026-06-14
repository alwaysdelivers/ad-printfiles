import requests, json, re
RAW='https://raw.githubusercontent.com/alwaysdelivers/ad-printfiles/main/'
catalog=json.load(open('/home/claude/_catalog.json'))   # {'71':{'col|size':id}, '146':{...}}
norm=lambda s: re.sub(r'[^a-z0-9]','',(s or '').lower())
COLOR_ALIAS={'athheather':'athleticheather'}            # shopify token -> printful (normalized)
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
 'karma_blueteal':{'light':'KARMA_blueteal_whitegarments.png','dark':'KARMA_blueteal_darkgarments.png','ar':0.579,'hoodie':(1650,440),'tee':(1600,470)},
 'karma_redwhite':{'light':None,'dark':'KARMA_redwhite_darkgarments.png','ar':0.579,'hoodie':(1650,440),'tee':(1600,470)},
 'sasquatch':{'light':'printfiles/SASQUATCH_sqt-01_whitegarments.png','dark':'printfiles/SASQUATCH_sqt-01_darkgarments.png','ar':0.671,'hoodie':(1680,420),'tee':(1600,500)},
 'caveman':{'light':'printfiles/CAVEMAN_cav-08_whitegarments.png','dark':'printfiles/CAVEMAN_cav-08_darkgarments.png','ar':0.681,'hoodie':(1680,420),'tee':(1600,500)},
 'snowman':{'light':'printfiles/SNOWMAN_snw-01_whitegarments.png','dark':'printfiles/SNOWMAN_snw-01_darkgarments.png','ar':0.755,'hoodie':(1500,420),'tee':(1400,500)},
 'stork':{'light':'printfiles/STORK_stk-07_whitegarments.png','dark':'printfiles/STORK_stk-07_darkgarments.png','ar':0.468,'hoodie':(1500,560),'tee':(1450,620)},
 'yeti':{'light':None,'dark':'printfiles/YETI_drawing_darkgarments.png','ar':1.283,'hoodie':(1150,250),'tee':(1350,440)},
 'usa250':{'light':'printfiles/AMERICA250_usa-250_whitegarments.png','dark':'printfiles/AMERICA250_usa-250_darkgarments.png','special':{'red':'printfiles/AMERICA250_usa-250_REDcharcoal.png'},'ar':0.687,'hoodie':(1600,440),'tee':(1500,500)},
}
# placements validated this session: all hoodies + KARMA tee. TEE creature/Stork tops are best-fit estimates -> spot-check.
UNVERIFIED_TEE=set()  # all verified on Men's 4 model
def design_of(title):
    t=title.lower()
    if 'karma' in t and 'red/white' in t: return 'karma_redwhite'
    if 'karma' in t: return 'karma_blueteal'
    for k in ('sasquatch','caveman','stork','yeti'):
        if k in t: return k
    if 'snowman' in t or 'abominable' in t: return 'snowman'
    if 'america' in t and '250' in t: return 'usa250'
    return None
def line_to_item(title,color,size,qty=1,retail=None,print_style=None):
    garment='hoodie' if 'hoodie' in title.lower() else 'tee'
    pid=146 if garment=='hoodie' else 71
    dk=design_of(title); d=DESIGNS[dk]
    ckey=COLOR_ALIAS.get(norm(color),norm(color))
    cv=catalog[str(pid)].get('%s|%s'%(ckey,norm(size)))
    if not cv: return {'error':'UNFULFILLABLE (no Printful blank)','title':title,'color':color,'size':size}
    fp=d['light'] if (ckey in LIGHT and d['light']) else d['dark']
    if d.get('special') and ckey in d['special']: fp=d['special'][ckey]
    if dk=='usa250' and (print_style or '').strip().lower()=='mono': fp='printfiles/AMERICA250_usa-250_MONO_%s.png'%_mono_ink(ckey)
    aw,ah=AREA[garment]; w,top=d[garment]; h=int(w*d['ar']); left=(aw-w)//2
    flags=[]
    if garment=='tee' and dk in UNVERIFIED_TEE: flags.append('TEE_PLACEMENT_UNVERIFIED')
    return {'variant_id':cv,'quantity':qty,'retail_price':retail,
            'files':[{'type':'front','url':RAW+fp,'position':{'area_width':aw,'area_height':ah,'width':w,'height':h,'top':top,'left':left}}],
            '_design':dk,'_garment':garment,'_file':fp,'_flags':flags}
