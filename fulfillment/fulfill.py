import requests, json, re
RAW='https://raw.githubusercontent.com/alwaysdelivers/ad-printfiles/main/'
catalog=json.load(open('/home/claude/_catalog.json'))   # {'71':{'col|size':id}, '146':{...}}
norm=lambda s: re.sub(r'[^a-z0-9]','',(s or '').lower())
COLOR_ALIAS={}                                          # shopify token -> printful (normalized); athheather retired 2026-07 (MOM standardized to 'Athletic Heather')
HOODIE_ALIAS={'athleticheather':'sportgrey'}            # Gildan 18500 grey name differs from Bella 3001
LIGHT={'white','sand','ash','tan','athleticheather','natural','sportgrey','silver','babyblue','babypink','softcream','carolinablue','lightblue','heathercarolinablue'}
SLATEC={'silver','ash','softcream','sand'}
WARM={'maroon','oxbloodblack','olive','militarygreen','forestgreen','heatheremerald'}

# ---- FULL-BLEED MODEL --------------------------------------------------------
# Print files are full-canvas with positioning baked in:
#   tee    = 3600x4800 (12x16"),  hoodie = 4200x4200 (14x14")
# Printful position area is expressed at 150dpi; the file fills the whole area.
AREA={'tee':(1800,2400),'hoodie':(2100,2100)}           # px150 print area
def fullbleed(garment):
    aw,ah=AREA[garment]
    return {'area_width':aw,'area_height':ah,'width':aw,'height':ah,'top':0,'left':0}
def PF(prefix, base, garment):                          # -> printfiles/<prefix>/<BASE>_<garment>.png
    return 'printfiles/%s/%s_%s.png'%(prefix, base, garment)
def ground(ckey): return 'light' if ckey in LIGHT else 'dark'


# ---- STYLE / INK RESOLUTION (live product truth; v33) ------------------------
JESUS_STYLES={'serif':'jes-01','script':'jes-03','bold':'jes-07','retro':'jes-11'}
MOM_STYLES={'grace':'mom-01','elegant':'mom-01','bold':'mom-03','retro':'mom-disco'}  # elegant: no art exists, routed to Grace as placeholder (2026-07-10) pending variant cleanup
DAD_STYLES={'classic':'dad-02','varsity':'dad-04','retro':'dad-disco'}
GOD_STYLES={'monument':'god-01','bold':'god-03','retro':'god-09'}
FAITH_STYLES={'elegant':'faith-02','bold':'faith-04','strong':'faith-04'}  # classic dropped; 'strong' = legacy alias for Bold (renamed 2026-07-10)
STORK_STYLES={'classic':'stk-07','elegant':'stk-01'}                        # 2 styles (v33)
AMERICA_STYLES={'classic','heritage','star','retro','watermark'}
CROSS_STYLES={'jesuscross':'cross-04','thecross':'cross-08'}

# faith-lane inks (fc/mono/red) -> file colorway suffix, by ground
def faithlane_cw(tk, ckey):
    if tk=='red':  return 'redmono'
    if tk=='mono': return ground(ckey)+'_mono'
    return ground(ckey)                                 # fc -> light/dark
FAITHLANE_INK={'full color':'fc','fullcolor':'fc','fc':'fc','mono':'mono','red':'red'}
FAITHLANE_VALID={'white':['fc','mono','red'],'athleticheather':['fc','mono','red'],'navy':['fc','mono','red'],'black':['fc','mono','red']}
# jesus inks (fc/navy/cream/red/black) -> file colorway; validity is STYLE-DEPENDENT (approved matrix 2026-07-09, 66/80)
JESUS_INK={'full color':'fc','fullcolor':'fc','fc':'fc','navy':'navy','cream':'cream','red':'red','black':'black'}
JESUS_VALID_BY_STYLE={"serif":{"white":["fc","navy","red","black"],"athleticheather":["fc","navy","red","black"],"navy":["fc","cream","red","black"],"black":["fc","navy","cream","red"]},"script":{"white":["fc","navy","red","black"],"athleticheather":["fc","navy","red","black"],"navy":["fc","cream","red","black"],"black":["fc","navy","cream","red"]},"bold":{"white":["fc","navy","red","black"],"athleticheather":["fc","navy","cream","red","black"],"navy":["fc","cream","red","black"],"black":["fc","navy","cream","red"]},"retro":{"white":["fc","navy","red","black"],"athleticheather":["fc","navy","cream","red","black"],"navy":["fc","cream","red","black"],"black":["fc","navy","cream","red"]}}
JESUS_DEFAULT={'white':'fc','athleticheather':'fc','navy':'fc','black':'fc'}   # fc valid in all 16 cells
def jesus_cw(tk, ckey):
    if tk=='navy':  return 'light_mono'
    if tk=='cream': return 'dark_mono'
    if tk=='red':   return 'redmono'
    if tk=='black': return 'blackmono'
    return ground(ckey)   # fc -> light/dark by ground
# stork inks (fc/navy/cream/red): navy = light-ground mono file, cream = dark-ground mono file
STORK_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','cream':'cream','red':'red'}
STORK_VALID={'white':['fc','navy','red'],'babypink':['fc','navy','red'],'babyblue':['fc','navy','red'],'black':['fc','cream','red']}
STORK_DEFAULT={'white':'fc','babypink':'fc','babyblue':'fc','black':'fc'}
def stork_cw(tk, ckey):
    if tk=='navy': return 'light_mono'
    if tk=='cream': return 'dark_mono'
    if tk=='red':  return 'redmono'
    return ground(ckey)   # fc -> light/dark by ground

# god/dad ink label -> treatment; treatment -> new file colorway
GD_INK={'fullcolor':'fc','full color':'fc','split':'fc','fc':'fc','navy':'navy','red':'red','black':'black',
        'cream':'cream','white':'white','heathergrey':'grey','heather grey':'grey','grey':'grey','gray':'grey',
        'karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
def gd_cw(tk, ckey):
    return ('fc_'+ground(ckey)) if tk=='fc' else tk     # fc -> fc_light/fc_dark; else literal
GOD_VALID_BY_STYLE={"monument":{"white":["fc","navy","red","black","neonblue"],"athleticheather":["fc","navy","red","black","neonblue"],"navy":["fc","red","black","cream","grey","neonblue"],"black":["fc","navy","red","cream","grey","neonblue"]},"bold":{"white":["fc","navy","red","black","neonblue"],"athleticheather":["fc","navy","red","black","cream","neonblue"],"navy":["fc","red","black","cream","grey","neonblue"],"black":["fc","navy","red","cream","grey","neonblue"]},"retro":{"white":["fc","navy","red","black","grey","neonblue"],"athleticheather":["fc","navy","red","black","cream","neonblue"],"navy":["fc","red","black","cream","grey","neonblue"],"black":["fc","navy","red","cream","grey","neonblue"]}}   # style-dependent (matrix 2026-07-09, 69/84)
GOD_DEFAULT={'white':'fc','athleticheather':'fc','navy':'fc','black':'fc'}   # fc valid in all 12 cells
# DAD validity is STYLE-DEPENDENT (approved matrix 2026-07-08): white ink on heather invalid for Classic only
DAD_VALID_BY_STYLE={"classic": {"athleticheather": ["fc", "red", "black", "navy", "neonblue"], "black": ["fc", "red", "navy", "white", "grey", "neonblue"], "navy": ["fc", "red", "black", "white", "grey", "neonblue"], "white": ["fc", "red", "black", "navy", "neonblue"]}, "retro": {"athleticheather": ["fc", "red", "black", "navy", "white", "neonblue"], "black": ["fc", "red", "navy", "white", "grey", "neonblue"], "navy": ["fc", "red", "black", "white", "grey", "neonblue"], "white": ["fc", "red", "black", "navy", "neonblue"]}, "varsity": {"athleticheather": ["fc", "red", "black", "navy", "white", "neonblue"], "black": ["fc", "red", "navy", "white", "grey", "neonblue"], "navy": ["fc", "red", "black", "white", "grey", "neonblue"], "white": ["fc", "red", "black", "navy", "neonblue"]}}
DAD_DEFAULT={'white':'fc','athleticheather':'fc','navy':'fc','black':'fc'}   # Full Color valid on every combo

# texas inks (single-ink per color, fc valid on light grounds only) -> file colorway
TEXAS_STYLES={'western':'western','classic':'classic','retro':'retro'}
TEXAS_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
TEXAS_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}   # identical across all 3 styles (2026-07-14)
TEXAS_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}   # fc never valid on dark grounds for this prefix
def texas_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk     # fc always fc_light (never valid on dark); else literal

# miami inks (single-ink per color, fc valid on light grounds only) -> file colorway - identical to TEXAS
MIAMI_STYLES={'western':'western','classic':'classic','retro':'retro'}
MIAMI_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
MIAMI_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}   # identical across all 3 styles (2026-07-14, cloned from TEXAS)
MIAMI_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def miami_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# vegas inks (single-ink per color, fc valid on light grounds only) -> file colorway - identical to TEXAS/MIAMI
VEGAS_STYLES={'western':'western','classic':'classic','retro':'retro'}
VEGAS_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
VEGAS_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
VEGAS_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def vegas_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# newyork inks (single-ink per color, fc valid on light grounds only) -> file colorway - identical to TEXAS/MIAMI/VEGAS
NEWYORK_STYLES={'western':'western','classic':'classic','retro':'retro'}
NEWYORK_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
NEWYORK_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
NEWYORK_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def newyork_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk
# newyork Flag + airport styles (2026-07-15). Flag: no ink, auto light/dark by ground; hoodie files carry _r2.
# Airports (ALB/BUF/JFK/LGA/ROC/SYR): tokens per STATE_BUILD_PROTOCOL §6 — fc_light White/AthHeather only;
# red/gold/neon(state)+white(code) dark only. Files: printfiles/stateairport/STATEAIRPORT_ny-<code>_<token>_<garment>.png
NEWYORK_AIRPORTS={'alb','buf','jfk','lga','roc','syr'}
NEWYORK_AIRPORT_INK={'fullcolor':'fc_light','full color':'fc_light','fc':'fc_light',
    'red':'redstate_white',
    'gold':'goldstate_white',
    'karmablue':'neonstate_white','karma blue':'neonstate_white','neon blue':'neonstate_white','neonblue':'neonstate_white'}
NEWYORK_AIRPORT_VALID={'white':['fc_light'],'athleticheather':['fc_light'],
    'navy':['redstate_white','goldstate_white','neonstate_white'],'black':['redstate_white','goldstate_white','neonstate_white']}
NEWYORK_AIRPORT_DEFAULT={'white':'fc_light','athleticheather':'fc_light','navy':'redstate_white','black':'redstate_white'}

# state Flag routing (2026-07-15): every merged state's Flag style + all plain-state products.
# Files: printfiles/states/{STATE}FLAG_{light|dark}_{garment}.png — hoodies carry _r2 (CDN fix).
STATE_FLAG_OF={'miami':'FLORIDAFLAG','vegas':'NEVADAFLAG','losangeles':'CALIFORNIAFLAG','chicago':'ILLINOISFLAG',
               'denver':'COLORADOFLAG','boston':'MASSACHUSETTSFLAG','seattle':'WASHINGTONFLAG','texas':'TEXASFLAG'}
TEXAS_AIRPORTS={'aus','dfw','hou','sat'}
TEXAS_AIRPORT_INK=NEWYORK_AIRPORT_INK          # same tokens/validity per STATE_BUILD_PROTOCOL §6
TEXAS_AIRPORT_VALID=NEWYORK_AIRPORT_VALID
TEXAS_AIRPORT_DEFAULT=NEWYORK_AIRPORT_DEFAULT
CHICAGO_AIRPORTS={'ord','mdw'}   # Illinois pilot 2026-07-15; files STATEAIRPORT_il-<code> (no _r2)
GEORGIA_STYLES={'western':'western','classic':'classic','retro':'retro'}
GEORGIA_AIRPORTS={'atl','sav'}   # wave 0 2026-07-15; files STATEAIRPORT_ga-<code> (no _r2)
def georgia_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# 41 plain-state flag products (2026-07-15). Elastic flag wave 2026-07-15: all flag files renamed (_r2 tee/_r3 hoodie). Titles like 'Alabama Always Delivers — Tee'.
# Matched LONGEST-FIRST ('west virginia' before 'virginia', 'arkansas' before 'kansas').
# Excludes the 9 merged states (texas + newyork + 7 renamed, handled above).
PLAIN_STATES=['west virginia','south carolina','south dakota','north carolina','north dakota',
 'new hampshire','new jersey','new mexico','rhode island','pennsylvania','mississippi','connecticut',
 'louisiana','minnesota','wisconsin','tennessee','arkansas','delaware','kentucky','maryland','michigan',
 'missouri','nebraska','oklahoma','virginia','alabama','arizona','indiana','montana','vermont',
 'wyoming','alaska','hawaii','kansas','oregon','idaho','maine','iowa','ohio','utah']
def plain_state_of(t):
    for s in PLAIN_STATES:
        if s in t: return s.replace(' ','')
    return None

# losangeles inks (single-ink per color, fc valid on light grounds only) -> file colorway - identical to TEXAS/MIAMI/VEGAS
LOSANGELES_STYLES={'western':'western','classic':'classic','retro':'retro'}
LOSANGELES_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
LOSANGELES_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
LOSANGELES_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def losangeles_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# chicago inks (single-ink per color, fc valid on light grounds only) -> file colorway - identical to TEXAS/MIAMI/VEGAS
CHICAGO_STYLES={'western':'western','classic':'classic','retro':'retro'}
CHICAGO_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
CHICAGO_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
CHICAGO_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def chicago_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# denver inks (single-ink per color, fc valid on light grounds only) -> file colorway - identical to TEXAS/MIAMI/VEGAS
DENVER_STYLES={'western':'western','classic':'classic','retro':'retro'}
DENVER_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
DENVER_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
DENVER_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def denver_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# boston inks (single-ink per color, fc valid on light grounds only) -> file colorway - identical to TEXAS/MIAMI/VEGAS
BOSTON_STYLES={'western':'western','classic':'classic','retro':'retro'}
BOSTON_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
BOSTON_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
BOSTON_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def boston_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# seattle inks (single-ink per color, fc valid on light grounds only) -> file colorway - identical to TEXAS/MIAMI/VEGAS
SEATTLE_STYLES={'western':'western','classic':'classic','retro':'retro'}
SEATTLE_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
SEATTLE_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
SEATTLE_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def seattle_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# grandpa inks (single-ink per color, fc valid on light grounds only) -> file colorway - identical structure to TEXAS/MIAMI/VEGAS
GRANDPA_STYLES={'western':'western','classic':'classic','retro':'retro'}
GRANDPA_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
GRANDPA_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
GRANDPA_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def grandpa_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# gameday inks (single-ink per color, fc valid on light grounds only) -> file colorway - Western/Varsity/Retro (NOT Classic)
GAMEDAY_STYLES={'western':'western','varsity':'varsity','retro':'retro'}
GAMEDAY_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
GAMEDAY_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
GAMEDAY_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def gameday_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# datenight inks (single-ink per color, fc valid on light grounds only) -> file colorway - only 2 styles (Romantic/Retro, no Western)
DATENIGHT_STYLES={'romantic':'romantic','retro':'retro'}
DATENIGHT_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
DATENIGHT_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
DATENIGHT_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def datenight_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# taco inks (single-ink per color, fc valid on light grounds only) -> file colorway - only 2 styles (Fiesta/Retro, no Western)
TACO_STYLES={'fiesta':'fiesta','retro':'retro'}
TACO_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
TACO_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
TACO_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def taco_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

# country inks (single-ink per color, fc valid on light grounds only) -> file colorway - only 2 styles (Western/Classic, no Retro)
COUNTRY_STYLES={'western':'western','classic':'classic'}
COUNTRY_INK={'fullcolor':'fc','full color':'fc','fc':'fc','navy':'navy','red':'red','black':'black','gold':'gold',
           'white':'white','karmablue':'neonblue','karma blue':'neonblue','neon blue':'neonblue','neonblue':'neonblue'}
COUNTRY_VALID={'white':['fc','navy','red','black','gold','neonblue'],'athleticheather':['fc','navy','red','black','gold','neonblue'],
             'navy':['red','gold','black','white','neonblue'],'black':['navy','red','gold','white','neonblue']}
COUNTRY_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}
def country_cw(tk, ckey):
    return 'fc_light' if tk=='fc' else tk

GRANDMA_STYLES={'grace':'grace','elegant':'elegant','retro':'retro'}
GRANDMA_INK={'navy':'navy','full color':'split','fullcolor':'split','black':'black','white':'white','red':'red','gold':'gold','neon blue':'karmablue','neonblue':'karmablue'}
GRANDMA_VALID={'white':['navy','split','black','red','gold','karmablue'],'athleticheather':['navy','split','black','red','gold','karmablue'],'navy':['white','red','gold','karmablue'],'black':['white','red','gold','karmablue']}
GRANDMA_DEFAULT={'white':'split','athleticheather':'split','navy':'white','black':'white'}

# america inks (single-ink per color) -> file colorway; ice removed, karmablue->neonblue
AMERICA_INK={'navy':'navy','red':'red','black':'black','gold':'gold','cream':'cream','white':'cream','grey':'grey','heather grey':'grey','heathergrey':'grey','karmablue':'neonblue','karma blue':'neonblue','neonblue':'neonblue','fullcolor':'fc','full color':'fc','fc':'fc'}
AMERICA_VALID={'white':['navy','red','black','gold','neonblue','fc'],'athleticheather':['navy','red','black','gold','neonblue','fc'],'navy':['cream','grey','red','gold','fc'],'black':['red','gold','cream','neonblue','grey','fc']}
AMERICA_DEFAULT={'white':'navy','athleticheather':'navy','navy':'cream','black':'red'}
def america_cw(tk, ckey):
    return ('fc_'+ground(ckey)) if tk=='fc' else tk

CROSS_INK={'full color':'fc','fullcolor':'fc','fc':'fc','mono':'mono','red':'red','full red':'red','heather grey':'grey','grey':'grey'}
CROSS_VALID={'cross-04':{'white':['fc','mono','red'],'athleticheather':['fc','mono','red'],'navy':['grey','red'],'black':['fc','mono','grey','red']},
             'cross-08':{'white':['fc','mono','red'],'athleticheather':['fc','mono','red'],'navy':['grey','red'],'black':['mono','grey','red']}}  # per-style (2026-07-10: The Cross x Black loses fc)
CROSS_DEFAULT={'white':'fc','athleticheather':'fc','navy':'red','black':'fc'}
CROSS_DEFAULT_08={'white':'fc','athleticheather':'fc','navy':'red','black':'red'}  # The Cross: Black default red (fc invalid)
def cross_cw(tk, ckey):
    return ('fc_'+ground(ckey)) if tk=='fc' else tk     # fc_light/fc_dark; mono/grey/red literal

CROWN_INK={'full color':'split','fullcolor':'split','split':'split','fc':'split','navy':'mono','slate':'mono','mono':'mono'}
CROWN_VALID={'white':['split','mono'],'athleticheather':['split','mono'],'navy':['mono'],'black':['mono']}  # mono token = Navy ink (light) or Slate ink (dark); same file

# creature inks (Full Color/Grey/Black) -> file suffix; validity per approved matrix 2026-07-10 (black-on-black struck)
CRE_INK={'fullcolor':'fc','fc':'fc','grey':'grey','gray':'grey','black':'black'}
CRE_VALID={'white':['fc','black'],'athleticheather':['fc','black'],'navy':['grey'],'black':['grey']}
CRE_DEFAULT={'white':'fc','athleticheather':'fc','navy':'grey','black':'grey'}
CRE_SUF={'fc':'whitegarments','grey':'darkgarments','black':'blackink'}
CROWN_DEFAULT={'white':'split','athleticheather':'split','navy':'mono','black':'mono'}
CROWN_COLOR={'white':'white','athleticheather':'heather','sportgrey':'heather','navy':'navy','black':'black'}

KARMA_STYLE_FILE={
 'blackblue':{'white':'KARMA_blackblue_neon','athleticheather':'KARMA_blackblue_neon','navy':'KARMA_blackblue_neon','black':'KARMA_blackblue_neon'},
 'blueteal':{'white':'KARMA_blueteal_teal','navy':'KARMA_blueteal_teal','black':'KARMA_blueteal_teal'},
 'bluecream':{'navy':'KARMA_bluewhite_blue','black':'KARMA_bluewhite_blue'},
 'redwhite':{'navy':'KARMA_redwhite_red','black':'KARMA_redwhite_red'},
 'slatewhite':{'navy':'KARMA_slatewhite_slate','black':'KARMA_slatewhite_slate'}}

def design_of(title):
    t=title.lower()
    if 'crown' in t: return 'crown'
    if 'cross' in t: return 'cross'
    if 'jesus' in t: return 'jesus'
    if 'faith' in t: return 'faith'
    if 'karma' in t: return 'karma'
    if 'mom' in t: return 'mom'
    if 'creature' in t: return 'creatures'
    for k in ('sasquatch','caveman','stork','yeti'):
        if k in t: return k
    if 'snowman' in t or 'abominable' in t: return 'snowman'
    if 'science' in t: return 'science'
    if 'dad' in t: return 'dad'
    if 'god' in t: return 'god'
    if 'america' in t: return 'america'
    if 'grandma' in t: return 'grandma'
    if 'texas' in t: return 'texas'
    if 'miami' in t or 'florida' in t: return 'miami'          # product renamed Florida (Option-2 merge); files stay city-named
    if 'vegas' in t or 'nevada' in t: return 'vegas'
    if 'newyork' in t or 'new york' in t: return 'newyork'   # title has a space (live: 'New York Always Delivers — Tee'); bare 'newyork' never matched (bug found 2026-07-15)
    if 'losangeles' in t or 'los angeles' in t or 'california' in t: return 'losangeles'
    if 'chicago' in t or 'illinois' in t: return 'chicago'
    if 'denver' in t or 'colorado' in t: return 'denver'
    if 'boston' in t or 'massachusetts' in t: return 'boston'
    if 'seattle' in t or 'washington' in t: return 'seattle'
    if 'georgia' in t: return 'georgia'
    _ps=plain_state_of(t)
    if _ps: return 'stateflag:'+_ps
    if 'grandpa' in t: return 'grandpa'
    if 'gameday' in t: return 'gameday'
    if 'datenight' in t: return 'datenight'
    if 'taco' in t: return 'taco'
    if 'country' in t: return 'country'
    return None

def _resolve_ink(label, table, valid, default, ckey):
    tk=table.get((label or '').strip().lower()) or table.get(norm(label))
    if not tk or tk not in valid.get(ckey,[]): tk=default.get(ckey)
    return tk

def line_to_item(title,color,size,qty=1,retail=None,print_style=None,ink=None,name=None):
    garment='hoodie' if 'hoodie' in title.lower() else 'tee'
    pid=146 if garment=='hoodie' else 71
    dk=design_of(title)
    ckey=COLOR_ALIAS.get(norm(color),norm(color))
    lookup_ckey=HOODIE_ALIAS.get(ckey,ckey) if garment=='hoodie' else ckey
    cv=catalog[str(pid)].get('%s|%s'%(lookup_ckey,norm(size)))
    if not cv: return {'error':'UNFULFILLABLE (no Printful blank)','title':title,'color':color,'size':size}
    def out(prefix, base, extra=None):
        item={'variant_id':cv,'quantity':qty,'retail_price':retail,
              'files':[{'type':'front','url':RAW+PF(prefix,base,garment),'position':fullbleed(garment)}],
              '_design':dk,'_garment':garment,'_file':PF(prefix,base,garment),'_flags':[]}
        if extra: item.update(extra)
        return item

    if dk=='jesus':
        st=norm(print_style); code=JESUS_STYLES.get(st)
        if not code: return {'error':'JESUS invalid Style','title':title,'style':print_style}
        jvalid=JESUS_VALID_BY_STYLE.get(st,{})
        tk=_resolve_ink(ink, JESUS_INK, jvalid, JESUS_DEFAULT, ckey)
        cw=jesus_cw(tk, ckey)
        return out('jesus', 'JESUS_%s_%s'%(code,cw))

    if dk in ('mom','faith'):
        STY={'mom':MOM_STYLES,'faith':FAITH_STYLES}[dk]
        st=norm(print_style); code=STY.get(st)
        if not code: return {'error':'%s invalid Style'%dk.upper(),'title':title,'style':print_style}
        tk=_resolve_ink(ink, FAITHLANE_INK, FAITHLANE_VALID, {'white':'fc','athleticheather':'fc','navy':'fc','black':'fc'}, ckey)
        cw=faithlane_cw(tk, ckey)
        PMAP={'mom':'MOM','faith':'FAITH'}
        return out(dk, '%s_%s_%s'%(PMAP[dk],code,cw))

    if dk=='stork':
        st=norm(print_style); code=STORK_STYLES.get(st)
        if not code: return {'error':'STORK invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, STORK_INK, STORK_VALID, STORK_DEFAULT, ckey)
        if not tk: return {'error':'STORK invalid ink','title':title,'ink':ink}
        cw=stork_cw(tk, ckey)
        return out('stork', 'STORK_%s_%s'%(code,cw))

    if dk in ('god','dad'):
        STY=GOD_STYLES if dk=='god' else DAD_STYLES
        DEF=GOD_DEFAULT if dk=='god' else DAD_DEFAULT
        st=norm(print_style); code=STY.get(st)
        if not code: return {'error':'%s invalid Style'%dk.upper(),'title':title,'style':print_style}
        VAL=GOD_VALID_BY_STYLE.get(st, {}) if dk=='god' else DAD_VALID_BY_STYLE.get(st, {})
        tk=_resolve_ink(ink, GD_INK, VAL, DEF, ckey)
        if not tk: return {'error':'%s invalid ink'%dk.upper(),'title':title,'ink':ink}
        cw=gd_cw(tk, ckey)
        return out(dk, '%s_%s_%s'%(dk.upper(),code,cw))

    if dk=='texas':
        st=norm(print_style)
        if st=='flag':
            fbase='%s_%s'%(STATE_FLAG_OF['texas'],ground(ckey))
            fpath='printfiles/states/%s_%s%s.png'%(fbase,garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        if st in TEXAS_AIRPORTS:
            tk=_resolve_ink(ink, TEXAS_AIRPORT_INK, TEXAS_AIRPORT_VALID, TEXAS_AIRPORT_DEFAULT, ckey)
            if not tk: return {'error':'TEXAS airport invalid ink','title':title,'ink':ink}
            fpath='printfiles/stateairport/STATEAIRPORT_tx-%s_%s_%s_r2.png'%(st,tk,garment)
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        code=TEXAS_STYLES.get(st)
        if not code: return {'error':'TEXAS invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, TEXAS_INK, TEXAS_VALID, TEXAS_DEFAULT, ckey)
        if not tk: return {'error':'TEXAS invalid ink','title':title,'ink':ink}
        cw=texas_cw(tk, ckey)
        return out('texas', 'TEXAS_%s_%s'%(code,cw))

    if dk=='georgia':
        st=norm(print_style)
        if st=='flag':
            fpath='printfiles/states/GEORGIAFLAG_%s_%s%s.png'%(ground(ckey),garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        if st in GEORGIA_AIRPORTS:
            tk=_resolve_ink(ink, NEWYORK_AIRPORT_INK, NEWYORK_AIRPORT_VALID, NEWYORK_AIRPORT_DEFAULT, ckey)
            if not tk: return {'error':'GEORGIA airport invalid ink','title':title,'ink':ink}
            fpath='printfiles/stateairport/STATEAIRPORT_ga-%s_%s_%s.png'%(st,tk,garment)
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        code=GEORGIA_STYLES.get(st)
        if not code: return {'error':'GEORGIA invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, NEWYORK_INK, NEWYORK_VALID, NEWYORK_DEFAULT, ckey)
        if not tk: return {'error':'GEORGIA invalid ink','title':title,'ink':ink}
        return out('georgia', 'GEORGIA_%s_%s'%(code, georgia_cw(tk, ckey)))

    if dk and dk.startswith('stateflag:'):
        scode=dk.split(':',1)[1].upper()+'FLAG'
        fpath='printfiles/states/%s_%s_%s%s.png'%(scode,ground(ckey),garment,'_r3' if garment=='hoodie' else '_r2')
        return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}

    if dk=='miami':
        st=norm(print_style)
        if st=='flag':
            fbase='%s_%s'%(STATE_FLAG_OF['miami'],ground(ckey))
            fpath='printfiles/states/%s_%s%s.png'%(fbase,garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        code=MIAMI_STYLES.get(st)
        if not code: return {'error':'MIAMI invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, MIAMI_INK, MIAMI_VALID, MIAMI_DEFAULT, ckey)
        if not tk: return {'error':'MIAMI invalid ink','title':title,'ink':ink}
        cw=miami_cw(tk, ckey)
        if code=='classic':   # classic files re-pushed as _r2 (suffix after garment; placement bug fixed 2026-07-15)
            fpath='printfiles/miami/MIAMI_%s_%s_%s_r2.png'%(code,cw,garment)
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        return out('miami', 'MIAMI_%s_%s'%(code,cw))

    if dk=='vegas':
        st=norm(print_style)
        if st=='flag':
            fbase='%s_%s'%(STATE_FLAG_OF['vegas'],ground(ckey))
            fpath='printfiles/states/%s_%s%s.png'%(fbase,garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        code=VEGAS_STYLES.get(st)
        if not code: return {'error':'VEGAS invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, VEGAS_INK, VEGAS_VALID, VEGAS_DEFAULT, ckey)
        if not tk: return {'error':'VEGAS invalid ink','title':title,'ink':ink}
        cw=vegas_cw(tk, ckey)
        if code=='classic':   # classic files re-pushed as _r2 (suffix after garment; placement bug fixed 2026-07-15)
            fpath='printfiles/vegas/VEGAS_%s_%s_%s_r2.png'%(code,cw,garment)
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        return out('vegas', 'VEGAS_%s_%s'%(code,cw))

    if dk=='newyork':
        st=norm(print_style)
        if st=='flag':
            base='NEWYORKFLAG_%s'%ground(ckey)
            fpath='printfiles/states/%s_%s%s.png'%(base,garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        if st in NEWYORK_AIRPORTS:
            tk=_resolve_ink(ink, NEWYORK_AIRPORT_INK, NEWYORK_AIRPORT_VALID, NEWYORK_AIRPORT_DEFAULT, ckey)
            if not tk: return {'error':'NEWYORK airport invalid ink','title':title,'ink':ink}
            return out('stateairport', 'STATEAIRPORT_ny-%s_%s'%(st,tk))
        code=NEWYORK_STYLES.get(st)
        if not code: return {'error':'NEWYORK invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, NEWYORK_INK, NEWYORK_VALID, NEWYORK_DEFAULT, ckey)
        if not tk: return {'error':'NEWYORK invalid ink','title':title,'ink':ink}
        cw=newyork_cw(tk, ckey)
        return out('newyork', 'NEWYORK_%s_%s'%(code,cw))

    if dk=='losangeles':
        st=norm(print_style)
        if st=='flag':
            fbase='%s_%s'%(STATE_FLAG_OF['losangeles'],ground(ckey))
            fpath='printfiles/states/%s_%s%s.png'%(fbase,garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        code=LOSANGELES_STYLES.get(st)
        if not code: return {'error':'LOSANGELES invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, LOSANGELES_INK, LOSANGELES_VALID, LOSANGELES_DEFAULT, ckey)
        if not tk: return {'error':'LOSANGELES invalid ink','title':title,'ink':ink}
        cw=losangeles_cw(tk, ckey)
        return out('losangeles', 'LOSANGELES_%s_%s'%(code,cw))

    if dk=='chicago':
        st=norm(print_style)
        if st in CHICAGO_AIRPORTS:
            tk=_resolve_ink(ink, NEWYORK_AIRPORT_INK, NEWYORK_AIRPORT_VALID, NEWYORK_AIRPORT_DEFAULT, ckey)
            if not tk: return {'error':'CHICAGO airport invalid ink','title':title,'ink':ink}
            fpath='printfiles/stateairport/STATEAIRPORT_il-%s_%s_%s.png'%(st,tk,garment)
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        if st=='flag':
            fbase='%s_%s'%(STATE_FLAG_OF['chicago'],ground(ckey))
            fpath='printfiles/states/%s_%s%s.png'%(fbase,garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        code=CHICAGO_STYLES.get(st)
        if not code: return {'error':'CHICAGO invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, CHICAGO_INK, CHICAGO_VALID, CHICAGO_DEFAULT, ckey)
        if not tk: return {'error':'CHICAGO invalid ink','title':title,'ink':ink}
        cw=chicago_cw(tk, ckey)
        return out('chicago', 'CHICAGO_%s_%s'%(code,cw))

    if dk=='denver':
        st=norm(print_style)
        if st=='flag':
            fbase='%s_%s'%(STATE_FLAG_OF['denver'],ground(ckey))
            fpath='printfiles/states/%s_%s%s.png'%(fbase,garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        code=DENVER_STYLES.get(st)
        if not code: return {'error':'DENVER invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, DENVER_INK, DENVER_VALID, DENVER_DEFAULT, ckey)
        if not tk: return {'error':'DENVER invalid ink','title':title,'ink':ink}
        cw=denver_cw(tk, ckey)
        return out('denver', 'DENVER_%s_%s'%(code,cw))

    if dk=='boston':
        st=norm(print_style)
        if st=='bos':   # MA wave 0b: BOS airport
            tk=_resolve_ink(ink, NEWYORK_AIRPORT_INK, NEWYORK_AIRPORT_VALID, NEWYORK_AIRPORT_DEFAULT, ckey)
            if not tk: return {'error':'MASSACHUSETTS airport invalid ink','title':title,'ink':ink}
            fpath='printfiles/stateairport/STATEAIRPORT_ma-bos_%s_%s.png'%(tk,garment)
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        if st=='flag':
            fbase='%s_%s'%(STATE_FLAG_OF['boston'],ground(ckey))
            fpath='printfiles/states/%s_%s%s.png'%(fbase,garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        code=BOSTON_STYLES.get(st)
        if not code: return {'error':'BOSTON invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, BOSTON_INK, BOSTON_VALID, BOSTON_DEFAULT, ckey)
        if not tk: return {'error':'BOSTON invalid ink','title':title,'ink':ink}
        cw=boston_cw(tk, ckey)
        if (name or '').strip().lower()=='massachusetts':   # MA wave 0b: Name line-item property routes state-name art
            return out('massachusetts', 'MASSACHUSETTS_%s_%s'%(code,cw))
        return out('boston', 'BOSTON_%s_%s'%(code,cw))

    if dk=='seattle':
        st=norm(print_style)
        if st=='flag':
            fbase='%s_%s'%(STATE_FLAG_OF['seattle'],ground(ckey))
            fpath='printfiles/states/%s_%s%s.png'%(fbase,garment,'_r3' if garment=='hoodie' else '_r2')
            return {'variant_id':cv,'quantity':qty,'retail_price':retail,
                    'files':[{'type':'front','url':RAW+fpath,'position':fullbleed(garment)}],
                    '_design':dk,'_garment':garment,'_file':fpath,'_flags':[]}
        code=SEATTLE_STYLES.get(st)
        if not code: return {'error':'SEATTLE invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, SEATTLE_INK, SEATTLE_VALID, SEATTLE_DEFAULT, ckey)
        if not tk: return {'error':'SEATTLE invalid ink','title':title,'ink':ink}
        cw=seattle_cw(tk, ckey)
        return out('seattle', 'SEATTLE_%s_%s'%(code,cw))

    if dk=='grandpa':
        st=norm(print_style); code=GRANDPA_STYLES.get(st)
        if not code: return {'error':'GRANDPA invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, GRANDPA_INK, GRANDPA_VALID, GRANDPA_DEFAULT, ckey)
        if not tk: return {'error':'GRANDPA invalid ink','title':title,'ink':ink}
        cw=grandpa_cw(tk, ckey)
        return out('grandpa', 'GRANDPA_%s_%s'%(code,cw))

    if dk=='gameday':
        st=norm(print_style); code=GAMEDAY_STYLES.get(st)
        if not code: return {'error':'GAMEDAY invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, GAMEDAY_INK, GAMEDAY_VALID, GAMEDAY_DEFAULT, ckey)
        if not tk: return {'error':'GAMEDAY invalid ink','title':title,'ink':ink}
        cw=gameday_cw(tk, ckey)
        return out('gameday', 'GAMEDAY_%s_%s'%(code,cw))

    if dk=='datenight':
        st=norm(print_style); code=DATENIGHT_STYLES.get(st)
        if not code: return {'error':'DATENIGHT invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, DATENIGHT_INK, DATENIGHT_VALID, DATENIGHT_DEFAULT, ckey)
        if not tk: return {'error':'DATENIGHT invalid ink','title':title,'ink':ink}
        cw=datenight_cw(tk, ckey)
        return out('datenight', 'DATENIGHT_%s_%s'%(code,cw))

    if dk=='taco':
        st=norm(print_style); code=TACO_STYLES.get(st)
        if not code: return {'error':'TACO invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, TACO_INK, TACO_VALID, TACO_DEFAULT, ckey)
        if not tk: return {'error':'TACO invalid ink','title':title,'ink':ink}
        cw=taco_cw(tk, ckey)
        return out('taco', 'TACO_%s_%s'%(code,cw))

    if dk=='country':
        st=norm(print_style); code=COUNTRY_STYLES.get(st)
        if not code: return {'error':'COUNTRY invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, COUNTRY_INK, COUNTRY_VALID, COUNTRY_DEFAULT, ckey)
        if not tk: return {'error':'COUNTRY invalid ink','title':title,'ink':ink}
        cw=country_cw(tk, ckey)
        return out('country', 'COUNTRY_%s_%s'%(code,cw))

    if dk=='grandma':
        st=norm(print_style); code=GRANDMA_STYLES.get(st)
        if not code: return {'error':'GRANDMA invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, GRANDMA_INK, GRANDMA_VALID, GRANDMA_DEFAULT, ckey)
        if not tk: return {'error':'GRANDMA invalid ink','title':title,'ink':ink}
        return out('grandma', 'GRANDMA_%s_%s'%(code,tk))

    if dk=='america':
        st=norm(print_style)
        if st not in AMERICA_STYLES: return {'error':'AMERICA invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, AMERICA_INK, AMERICA_VALID, AMERICA_DEFAULT, ckey)
        if not tk: return {'error':'AMERICA invalid ink','title':title,'ink':ink}
        cw=america_cw(tk, ckey)
        return out('america', 'AMERICA_%s_%s'%(st,cw))

    if dk=='cross':
        st=norm(print_style); code=CROSS_STYLES.get(st)
        if not code: return {'error':'CROSS invalid Style','title':title,'style':print_style}
        tk=_resolve_ink(ink, CROSS_INK, CROSS_VALID[code], CROSS_DEFAULT_08 if code=='cross-08' else CROSS_DEFAULT, ckey)
        cw=cross_cw(tk, ckey)
        return out('cross', 'CROSS_%s_%s'%(code,cw))

    if dk=='crown':
        cc=CROWN_COLOR.get(ckey)
        if not cc: return {'error':'CROWN unknown color','title':title,'color':color}
        tk=_resolve_ink(ink, CROWN_INK, CROWN_VALID, CROWN_DEFAULT, ckey)
        base=('CROWN_%s_split'%cc) if tk=='split' else ('CROWN_%s'%cc)
        return out('crown', base)

    if dk=='karma':
        st=norm(print_style); sf=KARMA_STYLE_FILE.get(st)
        if not sf: return {'error':'KARMA invalid Style','title':title,'style':print_style}
        kkey='athleticheather' if lookup_ckey=='sportgrey' else lookup_ckey
        base=sf.get(kkey) or sf.get(ckey)
        if not base: return {'error':'KARMA invalid Style x Color','title':title,'style':print_style,'color':color}
        return out('karma', base)

    if dk=='science':
        design=norm(print_style)
        if design not in ('physics','geometry','chemistry','algebra'):
            return {'error':'SCIENCE invalid Design','title':title,'design':print_style}
        SCI_INK={'navy':'navy','cream':'cream','red':'red','black':'black','sleet':'sleet',
                 'slate':'sleet','grey':'sleet','gray':'sleet','neon blue':'neonblue','neonblue':'neonblue','karma blue':'neonblue'}
        SCI_VALID={'white':['navy','black','red','neonblue'],'athleticheather':['navy','black','red','neonblue'],
                   'navy':['cream','sleet','red','neonblue'],'black':['cream','sleet','red','neonblue']}
        SCI_DEFAULT={'white':'navy','athleticheather':'navy','navy':'cream','black':'cream'}
        ink_cw=_resolve_ink(ink, SCI_INK, SCI_VALID, SCI_DEFAULT, ckey)
        return out('science', 'SCIENCE_%s_%s'%(design,ink_cw))

    # ---- creatures (combined) + standalone creature routes --------------------
    if dk=='creatures':
        cr=norm(print_style)
        if cr in ('yeti','yetiiceblue','yetiice','iceblue'):
            ice=(cr!='yeti') or (norm(ink or '') in ('ice','iceblue','blue'))
            base='YETI_ICE_allgarments' if ice else ('YETI_whitegarments' if ckey in LIGHT else 'YETI_darkgarments')
            return out('creatures', base)
        m={'caveman':'CAVEMAN','sasquatch':'SASQUATCH','abominablesnowman':'SNOWMAN','snowman':'SNOWMAN','abominable':'SNOWMAN'}.get(cr)
        if not m: return {'error':'CREATURES unknown design','title':title,'design':print_style}
        tk=_resolve_ink(ink, CRE_INK, CRE_VALID, CRE_DEFAULT, ckey)
        if not tk: return {'error':'CREATURES invalid ink','title':title,'ink':ink,'color':color}
        return out('creatures', '%s_%s'%(m, CRE_SUF[tk]))
    if dk in ('caveman','sasquatch','snowman'):
        m={'caveman':'CAVEMAN','sasquatch':'SASQUATCH','snowman':'SNOWMAN'}[dk]
        tk=_resolve_ink(ink, CRE_INK, CRE_VALID, CRE_DEFAULT, ckey)
        if not tk: return {'error':'%s invalid ink'%dk.upper(),'title':title,'ink':ink,'color':color}
        return out('creatures', '%s_%s'%(m, CRE_SUF[tk]))
    if dk=='yeti':
        ice=norm(print_style) in ('ice','iceblue','blue') or norm(ink or '') in ('ice','iceblue','blue')
        base='YETI_ICE_allgarments' if ice else ('YETI_whitegarments' if ckey in LIGHT else 'YETI_darkgarments')
        return out('creatures', base)

    return {'error':'unknown design','title':title}
