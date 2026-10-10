"""Allowlisted configuration studio transactions with stale-plan and undo guards."""
import copy, hashlib, re, time
import subcult_desktop as d
FILES=['workspaces.json','shell.json','subcult.json','visual.json']
PROTECTED={'subcult.workspaces','subcult.privacy','subcult.health','subcult.power','subcult.communications'}
VISUAL={'density':['compact','balanced','comfortable'],'opacity':['opaque','solid','soft'],'gaps':['tight','balanced','open'],'borders':['minimal','standard','strong']}
RECEIPT=d.STATE/'studio-last.json'

def raw(name):
    path=d.CONFIG/name
    if path.is_symlink():raise ValueError('Studio refuses symbolic-link configuration files')
    if not path.exists():return None
    if path.stat().st_size>262144:raise ValueError('Configuration file is too large')
    return path.read_text()

def source():
    result={}
    for name in FILES:
        raw(name)
        result[name]=d.config(name)
    return result

def projection(docs):
    workspaces=docs['workspaces.json'];bar=docs['shell.json'].get('bar',{})
    return {'schema_version':1,'display_mode':workspaces.get('display_mode','icon'),'workspaces':[{k:row.get(k) for k in ['id','name','icon','accent']} for row in workspaces.get('workspaces',[])],'layout':{section:[row['id'] for row in bar.get('layout',{}).get(section,[]) if isinstance(row,dict) and 'id' in row] for section in ['left','center','right']},'motion':docs['subcult.json'].get('motion',{}).get('mode','full'),'visual':{key:docs['visual.json'].get(key) for key in VISUAL}}

def validate(value,before):
    if not isinstance(value,dict) or value.get('schema_version')!=1:raise ValueError('Invalid preset')
    if set(value)!=set(before):raise ValueError('Unknown preset field')
    if value.get('display_mode') not in {'icon','number','name','auto'}:raise ValueError('Invalid workspace display mode')
    if value.get('motion') not in {'full','reduced','off'}:raise ValueError('Invalid motion mode')
    rows=value.get('workspaces');ids=set()
    if not isinstance(rows,list) or len(rows)!=10:raise ValueError('Preset must contain ten workspaces')
    for row in rows:
        if not isinstance(row,dict) or set(row)!= {'id','name','icon','accent'}:raise ValueError('Invalid workspace fields')
        n=row.get('id')
        if type(n)is not int or not 1<=n<=10 or n in ids:raise ValueError('Invalid workspace identity')
        ids.add(n);d.bounded_text(row.get('name'),40);d.bounded_text(row.get('icon'),8)
        if not isinstance(row.get('accent'),str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',row['accent']):raise ValueError('Invalid workspace accent')
    layout=value.get('layout')
    if not isinstance(layout,dict) or set(layout)!= {'left','center','right'}:raise ValueError('Invalid bar sections')
    all_ids=[];known={n for rows in before['layout'].values() for n in rows}
    for section,rows in layout.items():
        if not isinstance(rows,list) or len(rows)>40 or any(not isinstance(n,str) or n not in known for n in rows):raise ValueError('Unknown bar widget')
        all_ids+=rows
    if len(all_ids)!=len(set(all_ids)):raise ValueError('Duplicate bar widget')
    if not (PROTECTED&known)<=set(all_ids):raise ValueError('Required indicators cannot be removed')
    if not isinstance(value.get('visual'),dict) or set(value['visual'])!=set(VISUAL):raise ValueError('Invalid visual fields')
    if any(value['visual'][key] not in choices for key,choices in VISUAL.items()):raise ValueError('Invalid visual choice')
    return value

def state():
    current=projection(source());return {'preset':current,'visual_choices':VISUAL,'protected':sorted(PROTECTED),'undo_available':RECEIPT.is_file()}

def preview(value):
    docs=source();before=projection(docs);validate(value,before)
    hashes={name:hashlib.sha256((raw(name) or '').encode()).hexdigest() for name in FILES}
    changes=[{'field':key,'before':before[key],'after':value[key]} for key in before if before[key]!=value[key]]
    return d.plan({'preset':value,'before':before,'file_hashes':hashes,'changes':changes,'expires_note':'Plans expire in the browser after five minutes and become invalid when files change.'})

def documents(value,docs):
    docs=copy.deepcopy(docs);by_id={row['id']:row for row in value['workspaces']}
    for row in docs['workspaces.json']['workspaces']:row.update(by_id[row['id']])
    docs['workspaces.json']['display_mode']=value['display_mode']
    existing={row['id']:row for rows in docs['shell.json']['bar']['layout'].values() if isinstance(rows,list) for row in rows if isinstance(row,dict) and 'id' in row}
    docs['shell.json']['bar']['layout'].update({section:[existing[n] for n in rows] for section,rows in value['layout'].items()})
    docs['subcult.json'].setdefault('motion',{})['mode']=value['motion'];docs['visual.json'].update(value['visual'])
    return docs

def refresh():
    return [argv[0] for argv in [['subcult-motion','apply'],['hyprctl','reload'],['omarchy-shell','shell','rescanPlugins']] if d.run(argv,timeout=8) is None]

def restore_files(values):
    # Restore parsed JSON exactly in meaning; absent files remain absent.
    import json
    for name,value in values.items():
        raw(name)
        if value is None:(d.CONFIG/name).unlink(missing_ok=True)
        else:d.atomic(d.CONFIG/name,json.loads(value))

def apply(value,token):
    with d.lock('studio'):
        plan=preview(value);d.confirm(plan,token)
        if not plan['changes']:return {'status':'unchanged'}
        old={name:raw(name) for name in FILES};docs=documents(value,source())
        try:
            for name in FILES:d.atomic(d.CONFIG/name,docs[name])
        except BaseException:
            restore_files(old);raise
        record={'before':old,'after_hashes':{name:hashlib.sha256(raw(name).encode()).hexdigest() for name in FILES},'at':int(time.time())}
        d.atomic(RECEIPT,record)
        warnings=refresh();d.run(['subcult-journal','event','recipe','--label','Configuration studio'],timeout=1)
        return {'status':'applied','undo_available':True,'runtime_unavailable':warnings}

def undo():
    with d.lock('studio'):
        record=d.read(RECEIPT)
        if not isinstance(record,dict):raise ValueError('No studio transaction to undo')
        for name,expected in record['after_hashes'].items():
            if hashlib.sha256((raw(name) or '').encode()).hexdigest()!=expected:raise ValueError('Configuration changed after apply; undo refused to protect newer edits')
        restore_files(record['before']);RECEIPT.unlink();return {'status':'undone','runtime_unavailable':refresh()}
