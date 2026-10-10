"""Shared local desktop configuration, process probes and confirmation helpers."""
import contextlib
import fcntl
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", Path.home()/".config"))/"omarchy"
STATE = Path(os.environ.get("XDG_STATE_HOME", Path.home()/".local/state"))/"subcult-rice"

def read(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return default

def defaults(name):
    for path in (ROOT/"omarchy"/name, Path.home()/".local/share/subcult-rice"/name):
        if path.is_file():
            return read(path)
    raise ValueError("Default configuration unavailable: "+name)

def config(name):
    path=CONFIG/name
    if path.exists():
        value=read(path)
        if not isinstance(value,dict):
            raise ValueError("Invalid configuration: "+name)
        return value
    return defaults(name)

def atomic(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix="."+path.name+".",dir=path.parent)
    try:
        with os.fdopen(fd,"w") as stream:
            json.dump(value,stream,indent=2,ensure_ascii=False);stream.write("\n")
            stream.flush();os.fsync(stream.fileno())
        os.chmod(tmp,0o600);os.replace(tmp,path)
    finally:
        Path(tmp).unlink(missing_ok=True)

@contextlib.contextmanager
def lock(name):
    STATE.mkdir(parents=True,exist_ok=True)
    path=STATE/(name+".lock")
    with path.open("a+") as handle:
        os.chmod(path,0o600);fcntl.flock(handle,fcntl.LOCK_EX)
        yield

def run(argv, timeout=3, **kwargs):
    try:
        result=subprocess.run(argv,capture_output=True,text=True,timeout=timeout,**kwargs)
        if result.returncode:
            return None
        return result.stdout.strip()
    except (OSError,subprocess.SubprocessError):
        return None

def probe(argv, default=None):
    try:
        return json.loads(run(argv) or "")
    except ValueError:
        return default

def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()[:24]

def plan(value):
    return {**value,"plan_id":fingerprint(value),"read_only":True}

def confirm(value, token):
    if token != value["plan_id"]:
        raise ValueError("Plan changed; preview again and confirm the current plan_id")

def emit(value):
    print(json.dumps(value,ensure_ascii=False,separators=(",",":")))

def event(category,summary,source):
    run(["subcult-operations-log","record",category,summary,"--source",source],timeout=1)

def bounded_text(value, limit=80):
    if not isinstance(value,str) or not value.strip() or len(value)>limit or any(ord(c)<32 for c in value):
        raise ValueError("Invalid text field")
    return value.strip()

def document(name):
    for path in (ROOT/name,Path.home()/".local/share/subcult-rice"/name):
        if path.is_file():
            return path
    raise ValueError("Document unavailable: "+name)
