"""Bounded workspace dashboard projections. No task-provider commands or remote fetches."""
from urllib.parse import urlsplit
import subcult_desktop as d

def text(value,limit=100):
    return d.bounded_text(value,limit)

def safe_link(row):
    if not isinstance(row,dict):raise ValueError('Invalid link')
    url=text(row.get('url'),2048);parsed=urlsplit(url)
    if parsed.scheme not in {'http','https'} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:raise ValueError('Links require credential-free HTTP(S) URLs without query or fragment')
    return {'label':text(row.get('label')),'url':url}

def policy():
    value=d.config('dashboard.json')
    if value.get('schema_version')!=1:raise ValueError('Invalid dashboard schema')
    result={}
    for key in ['links','tasks','builds']:
        rows=value.get(key,[])
        if not isinstance(rows,list) or len(rows)>40:raise ValueError('Dashboard collection too large')
        result[key]=[]
        for row in rows:
            if not isinstance(row,dict):raise ValueError('Invalid dashboard row')
            workspaces=row.get('workspaces',[])
            if not isinstance(workspaces,list) or any(type(n)is not int or not 1<=n<=10 for n in workspaces):raise ValueError('Invalid dashboard workspace')
            clean=safe_link(row) if key=='links' else {'label':text(row.get('label')),'state':text(row.get('state','pending'),24)}
            if key=='tasks' and clean['state'] not in {'pending','active','done'}:raise ValueError('Invalid task state')
            if key=='builds' and clean['state'] not in {'pending','running','passed','failed','unknown'}:raise ValueError('Invalid build state')
            if key!='links':clean['updated_at']=row.get('updated_at') if type(row.get('updated_at')) is int and row['updated_at']>=0 else None
            clean['workspaces']=workspaces;result[key].append(clean)
    return result

def identity(workspace_id):
    try:
        value=d.config('workspaces.json')
        row=next((x for x in value.get('workspaces',[]) if x.get('id')==workspace_id),{})
        return text(row.get('name',f'Workspace {workspace_id}'),40)
    except (ValueError,AttributeError,TypeError):return f'Workspace {workspace_id}'

def surface(workspace_id,thermal=None,online=True):
    try:config=policy();error=None
    except ValueError:config={'links':[],'tasks':[],'builds':[]};error='Invalid dashboard configuration'
    try:
        kits=d.config('workspace-kits.json').get('kits',[])
        kit=next((r for r in kits if r.get('id')==workspace_id),{})
        tools=[text(row.get('label'),60) for row in kit.get('apps',[])][:8]
        links=[safe_link(row) for row in kit.get('links',[])][:12]
    except (ValueError,AttributeError,TypeError):tools=[];links=[]
    def selected(key):return [r for r in config[key] if not r['workspaces'] or workspace_id in r['workspaces']][:8]
    links+=selected('links');seen=set();unique=[]
    for row in links:
        if row['url'] not in seen:unique.append(row);seen.add(row['url'])
    attention=[]
    if thermal and thermal.get('available') and thermal.get('tier') in {'warning','critical','emergency'}:attention.append({'label':'Sustained thermal warning' if thermal.get('alerted') else 'Elevated temperature; check sustained warning state','state':'warning'})
    if not online:attention.append({'label':'Network link unavailable','state':'warning'})
    if error:attention.append({'label':error,'state':'unavailable'})
    builds=selected('builds')
    for row in builds:
        if row['state']=='failed':attention.append({'label':'Build failed: '+row['label'],'state':'warning'})
    return {'schema_version':1,'workspace':workspace_id,'label':identity(workspace_id) if workspace_id else 'Workspace unavailable','tools':tools,'links':unique[:12],'tasks':selected('tasks'),'builds':builds,'attention':attention[:6],'provider':'local configuration; timestamps supplied by your task/build exporter','read_only':True}
