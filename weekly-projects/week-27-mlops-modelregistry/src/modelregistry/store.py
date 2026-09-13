from __future__ import annotations
import hashlib,json,shutil,sqlite3,time
from pathlib import Path

SCHEMA="""
CREATE TABLE IF NOT EXISTS model_versions(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 version INTEGER NOT NULL,
 artifact_path TEXT NOT NULL,
 sha256 TEXT NOT NULL,
 signature_json TEXT NOT NULL,
 metrics_json TEXT NOT NULL,
 tags_json TEXT NOT NULL,
 data_hash TEXT NOT NULL,
 code_revision TEXT NOT NULL,
 run_id TEXT NOT NULL,
 created_at REAL NOT NULL,
 UNIQUE(name,version)
);
CREATE TABLE IF NOT EXISTS aliases(
 name TEXT NOT NULL,
 alias TEXT NOT NULL,
 version INTEGER NOT NULL,
 updated_at REAL NOT NULL,
 PRIMARY KEY(name,alias)
);
CREATE TABLE IF NOT EXISTS audit(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 event TEXT NOT NULL,
 name TEXT NOT NULL,
 version INTEGER,
 detail TEXT,
 created_at REAL NOT NULL
);
"""

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(65536),b""):h.update(chunk)
    return h.hexdigest()

class Registry:
    def __init__(self,db_path,store_path):
        self.db_path=Path(db_path);self.store_path=Path(store_path)
        self.db_path.parent.mkdir(parents=True,exist_ok=True);self.store_path.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(self.db_path) as c:c.executescript(SCHEMA)
    def _next_version(self,name):
        with sqlite3.connect(self.db_path) as c:
            row=c.execute("SELECT COALESCE(MAX(version),0)+1 FROM model_versions WHERE name=?",(name,)).fetchone()
        return int(row[0])
    def register(self,name,artifact,signature,metrics,tags,data_hash,code_revision,run_id):
        version=self._next_version(name);src=Path(artifact)
        dst_dir=self.store_path/name/f"v{version}";dst_dir.mkdir(parents=True,exist_ok=False)
        dst=dst_dir/src.name;shutil.copy2(src,dst);digest=sha256(dst)
        now=time.time()
        with sqlite3.connect(self.db_path) as c:
            c.execute("""INSERT INTO model_versions(name,version,artifact_path,sha256,signature_json,metrics_json,tags_json,data_hash,code_revision,run_id,created_at)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)""",(name,version,str(dst),digest,json.dumps(signature),json.dumps(metrics),json.dumps(tags),data_hash,code_revision,run_id,now))
            c.execute("INSERT INTO audit(event,name,version,detail,created_at) VALUES(?,?,?,?,?)",("register",name,version,digest,now))
        return version
    def get(self,name,version):
        with sqlite3.connect(self.db_path) as c:
            r=c.execute("SELECT artifact_path,sha256,signature_json,metrics_json,tags_json,data_hash,code_revision,run_id FROM model_versions WHERE name=? AND version=?",(name,version)).fetchone()
        if not r:raise KeyError((name,version))
        return {"name":name,"version":version,"artifact_path":r[0],"sha256":r[1],"signature":json.loads(r[2]),"metrics":json.loads(r[3]),"tags":json.loads(r[4]),"data_hash":r[5],"code_revision":r[6],"run_id":r[7]}
    def verify_artifact(self,name,version):
        m=self.get(name,version);return sha256(m["artifact_path"])==m["sha256"]
    def set_alias(self,name,alias,version):
        self.get(name,version)
        now=time.time()
        with sqlite3.connect(self.db_path) as c:
            c.execute("""INSERT INTO aliases(name,alias,version,updated_at) VALUES(?,?,?,?)
            ON CONFLICT(name,alias) DO UPDATE SET version=excluded.version,updated_at=excluded.updated_at""",(name,alias,version,now))
            c.execute("INSERT INTO audit(event,name,version,detail,created_at) VALUES(?,?,?,?,?)",("alias",name,version,alias,now))
    def resolve_alias(self,name,alias):
        with sqlite3.connect(self.db_path) as c:r=c.execute("SELECT version FROM aliases WHERE name=? AND alias=?",(name,alias)).fetchone()
        if not r:raise KeyError((name,alias))
        return self.get(name,int(r[0]))
    def audit_events(self,name):
        with sqlite3.connect(self.db_path) as c:
            return c.execute("SELECT event,version,detail FROM audit WHERE name=? ORDER BY id",(name,)).fetchall()
