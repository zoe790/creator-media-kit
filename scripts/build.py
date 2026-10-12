#!/usr/bin/env python3
"""Build eight offline creator media-kit HTML layouts. Python 3 standard library."""
import argparse, html, json, re, shutil, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
STYLES=json.loads((ROOT/'assets/styles.json').read_text())
def esc(v): return html.escape(str(v),quote=True)
def build(inp,out,styles='all',mode='full'):
    inp=Path(inp).resolve(); out=Path(out).resolve()
    d=json.loads(inp.read_text(encoding='utf-8')); profile=d.get('profile',{})
    if not profile.get('name'): raise ValueError('profile.name is required')
    if mode not in ('preview','full'): raise ValueError('mode must be preview or full')
    brand_limit=d.get('settings',{}).get('brand_limit',6)
    if type(brand_limit) is not int or brand_limit<0:raise ValueError('settings.brand_limit must be a non-negative integer')
    selected=STYLES if styles=='all' else [s for s in STYLES if s['slug'] in styles.split(',')]
    if not selected or (styles!='all' and set(styles.split(','))!={s['slug'] for s in selected}): raise ValueError('Unknown style')
    brands=d.get('brands',[]); cases=d.get('cases',[])
    for seq in (brands,cases):
        ids=[x.get('id') for x in seq]
        if None in ids or len(ids)!=len(set(ids)): raise ValueError('IDs must be present and unique')
    bm={b['id']:b for b in brands}; cm={c['id']:c for c in cases}
    for c in cases:
        if c.get('kind') not in ('sponsored','editorial','unknown'): raise ValueError('case.kind must be sponsored, editorial or unknown')
        if c.get('brand_id') and c['brand_id'] not in bm: raise ValueError('Unknown case brand_id')
        if c['kind']=='sponsored' and c.get('brand_id') and bm[c['brand_id']].get('confirmed') is not True: raise ValueError('Sponsored brands require confirmed:true')
    sections=d.get('sections')
    if sections is None:
        sections=[{'title':title,'case_ids':[c['id'] for c in cases if c['kind']==kind]} for kind,title in [('sponsored','Brand collaborations'),('editorial','Independent work'),('unknown','Content showcase')]]
        sections=[s for s in sections if s['case_ids']]
    assigned=[]
    for sec in sections:
        for cid in sec.get('case_ids',[]):
            if cid not in cm: raise ValueError('Unknown section case ID: '+str(cid))
            assigned.append(cid)
    # Preserve unassigned evidence rather than silently discard it.
    rest=[c['id'] for c in cases if c['id'] not in assigned]
    if rest: sections=sections+[{'title':'More work','case_ids':rest}]
    out.mkdir(parents=True,exist_ok=True)
    if (out/'manifest.json').exists(): raise ValueError('Output already exists; use a new version directory')
    assets=out/'assets'; assets.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets/fonts',assets/'fonts',dirs_exist_ok=True)
    shutil.copytree(ROOT/'assets/licenses',assets/'licenses',dirs_exist_ok=True)
    copied={}
    def asset(path):
        if not path:return ''
        src=Path(path).expanduser(); src=src if src.is_absolute() else inp.parent/src
        src=src.resolve()
        if not src.is_file():raise ValueError('Missing asset: '+str(src))
        if src.suffix.lower() not in ('.png','.jpg','.jpeg','.webp','.svg','.avif'):raise ValueError('Unsupported image: '+str(src))
        # SVGs must be trusted static assets, never HTML/script containers.
        if src.suffix.lower()=='.svg':
            raw=src.read_text()
            if re.search(r'<script|<foreignObject|\bon\w+\s*=|(?:href|src)\s*=\s*[\"\x27](?:https?:|javascript:|data:text)',raw,re.I):raise ValueError('Use a trusted static SVG or raster image')
        key=hashlib.sha256(src.read_bytes()).hexdigest()[:16]+src.suffix.lower()
        if key not in copied:shutil.copy2(src,assets/key);copied[key]=True
        return '../assets/'+key
    photo=d.get('photos') or {}; original=asset(photo.get('original')); cutout=asset(photo.get('cutout'))
    for b in brands:b['_src']=asset(b.get('logo'))
    for c in cases:c['_src']=asset(c.get('image'))
    def logo(b):
        return '<img class="brand-image" src="'+b['_src']+'" alt="'+esc(b['name'])+'">' if b.get('_src') else '<span class="brand-name">'+esc(b['name'])+'</span>'
    def cards(ids):
        result=[]
        for cid in ids:
            c=cm[cid]; b=bm.get(c.get('brand_id')); title=c.get('title','')
            has_brand=b and b.get('confirmed') is True and c['kind']=='sponsored'
            kind_label={'sponsored':'Brand collaboration','editorial':'Independent work','unknown':'Content showcase'}[c['kind']]
            top=logo(b) if has_brand else '<span class="brand-name">'+kind_label+'</span>'
            kind_line='<div class="case-kind">'+kind_label+'</div>' if has_brand else ''
            shot='<img class="original" src="'+c['_src']+'" alt="'+esc(title)+'">' if c['_src'] else '<div class="missing-image">Case image not supplied</div>'
            metrics=''.join('<span>'+esc(m['label'])+' '+esc(m['value'])+'</span>' for m in c.get('metrics',[]) if m.get('show') is True and m.get('value') is not None)
            result.append('<article class="card" data-case="'+esc(cid)+'"><div class="card-head"><div class="logo-stage">'+top+'</div>'+kind_line+'</div>'+shot+'<div class="caption">'+esc(title)+'</div><div class="metrics">'+metrics+'</div></article>')
        return ''.join(result)
    accounts=[a for a in profile.get('accounts',[]) if a.get('platform') and a.get('followers') is not None and str(a['followers']).strip()]
    def stats(seq,cls='stats'):
        return '<div class="'+cls+'" style="grid-template-columns:repeat('+str(min(3,max(1,len(seq))))+',1fr)">'+''.join('<div class="stat"><span class="stat-label">'+esc(a['platform'])+' followers</span><span class="stat-value">'+esc(a['followers'])+'</span></div>' for a in seq)+'</div>'
    name=str(profile['name']); namehtml=esc(name)
    if '\n' in name:namehtml='<br>'.join(esc(x) for x in name.splitlines())
    roles='<div class="identity">'+'<br>'.join(esc(x) for x in profile.get('roles',[]))+'</div>'
    tags='<div class="tags">'+''.join('<span>'+esc(x)+'</span>' for x in profile.get('tags',[]))+'</div>'
    common=(ROOT/'assets/templates/common.css').read_text()
    entries=[]
    for s in selected:
        slug=s['slug']; dest=out/slug;dest.mkdir(exist_ok=True)
        portrait=(original or cutout) if s['portrait_mode']=='framed' else (cutout or original)
        cls='has-photo' if portrait else 'no-photo'
        if portrait and not cutout and s['portrait_mode']=='overlap':cls+=' original-only'
        if photo.get('fit')=='contain':cls+=' portrait-contain'
        values=dict(name=esc(name),name_html=namehtml,location=esc(profile.get('location','')),bio=esc(profile.get('bio','')),description=esc(profile.get('description','')),roles=roles,tags=tags,stats=stats(accounts[:3]),portrait_src=portrait)
        hero=(ROOT/f'assets/templates/{slug}.html').read_text()
        for k,v in values.items():hero=hero.replace('{{'+k+'}}',v)
        if not portrait:
            words={'pink-sticker':'About Me','pink-scrapbook':'CREATOR','navy-creator':'PORTFOLIO','cream-ugc':'Life & ideas.','cocoa-retro':'creative portfolio','red-editorial':'portfolio.','long-table':'Life, ideas & things I build.','editorial-tri-tone':'CREATOR / MEDIA KIT'}
            hero='<div class="masthead"><span>'+esc(name)+' · Creator media kit</span><span class="kicker">'+esc(profile.get('location',''))+'</span></div><div class="np-word">'+words[slug]+'</div><div class="hero-copy"><h1 class="hero-title">'+esc(name).replace('\n','<br>')+'</h1>'+roles+tags+'</div>'+stats(accounts[:3])+'<div class="hero-foot">'+esc(profile.get('bio',''))+'<br>'+esc(profile.get('description',''))+'</div>' 
        if '{{' in hero:raise ValueError('Unresolved template token '+slug)
        main='<header class="hero">'+hero+'</header>'
        if len(accounts)>3:main+='<section class="extra-platforms"><h3>Other platforms</h3>'+stats(accounts[3:],'extra-stats')+'</section>'
        secs=sections[:1] if mode=='preview' else sections
        for i,sec in enumerate(secs):
            ids=sec.get('case_ids',[])[:3] if mode=='preview' else sec.get('case_ids',[])
            main+='<section class="case-section"><div class="case-head"><div class="kicker">'+f'{i+1:02d} / SELECTED WORK'+'</div><h2>'+esc(sec.get('title','Brand collaborations'))+'</h2><p>'+esc(sec.get('subtitle',''))+'</p></div><div class="case-grid">'+cards(ids)+'</div></section>'
        confirmed=[b for b in brands if b.get('confirmed') is True]
        showbrands=confirmed[:brand_limit] if brand_limit else confirmed
        brand_title='Selected brand partners' if len(showbrands)<len(confirmed) else 'Brand partners'
        if showbrands:main+='<section class="brand-section"><h3>'+brand_title+'</h3><div class="brand-grid" style="grid-template-columns:repeat('+str(min(6,len(showbrands)))+',1fr)">'+''.join('<div class="brand-cell">'+logo(b)+'</div>' for b in showbrands)+'</div></section>'
        contact=profile.get('contact',[])
        footer=' · '.join(esc(c['label'])+': '+esc(c['value']) for c in contact)
        notes=[]
        if mode=='preview':notes.append('Preview: introduction and up to 3 cases from the first group')
        dates=list(dict.fromkeys(str(a['platform'])+' '+str(a['as_of']) for a in accounts if a.get('as_of')))
        if dates:notes.append('Data observed: '+' / '.join(dates))
        if d.get('delivery_note'):notes.append(str(d['delivery_note']))
        if notes:footer+=''.join(('<br>' if footer or i else '')+esc(note) for i,note in enumerate(notes))
        if d.get('demo'):footer='Fictional demo: sample accounts and collaborations'+(' · '+footer if footer else '')
        if footer:main+='<footer class="contact">'+footer+'</footer>'
        css=(ROOT/f'assets/templates/{slug}.css').read_text()+'\n'+common
        links=''.join('<link rel="stylesheet" href="../assets/fonts/'+f+'">' for f in ['long-table-fonts.css','editorial-tri-tone-fonts.css','creative-mode-fonts.css','preview-fonts.css'])
        doc='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=1080"><title>'+esc(name)+' · '+esc(s['name'])+'</title>'+links+'<style>'+css+'</style><body><main id="poster" class="'+cls+'" data-style="'+slug+'">'+main+'</main></body></html>'
        (dest/'poster.html').write_text(doc,encoding='utf-8')
        entries.append({'style':slug,'name':s['name'],'html':slug+'/poster.html','png':slug+'/poster.png','jpg':slug+'/poster.jpg'})
    manifest={'mode':mode,'styles':entries,'case_count':len(cases),'brand_count':len([b for b in brands if b.get('confirmed') is True]),'displayed_brand_count':len(showbrands),'photo_mode':'provided' if original or cutout else 'none'}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    # Preserve provenance and the editable brief privately with the user's deliverable.
    clean=json.loads(inp.read_text());(out/'source-brief.json').write_text(json.dumps(clean,ensure_ascii=False,indent=2))
    (out/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Beyond the Feed | Style overview</title><style>body{background:#e6e2db;font:18px sans-serif;padding:24px}.grid{display:grid;grid-template-columns:repeat('+str(min(4,len(entries)))+',1fr);gap:24px}img{width:100%}a{color:#222;text-decoration:none}h2{font-size:20px}.project-header{padding:12px 0 32px;border-bottom:1px solid #bfb8ae;margin-bottom:28px}.project-header h1{font-size:64px;letter-spacing:-3px;line-height:1.1;margin:0 0 16px}.project-header p{font-size:28px;margin:0;color:#62564c}.project-header strong{color:#2c2824}</style><header class="project-header"><h1>Beyond the Feed</h1><p><strong>Seen to Signed.</strong> Turn your content into a portfolio worth sharing.</p></header><div class="grid">'+''.join('<a href="'+x['html']+'"><h2>'+esc(x['name'])+'</h2><img src="'+x['png']+'"></a>' for x in entries)+'</div>')
    return manifest
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);ap.add_argument('--styles',default='all');ap.add_argument('--mode',default='full',choices=['full','preview']);a=ap.parse_args()
    try: print(json.dumps(build(a.input,a.output,a.styles,a.mode),ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError) as e:ap.exit(2,'Build failed: '+str(e)+'\n')
