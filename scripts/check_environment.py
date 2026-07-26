from __future__ import annotations
from importlib import metadata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for line in (ROOT/"requirements.lock.txt").read_text().splitlines():
 if not line.strip() or line.startswith("#"): continue
 name,version=line.split("==",1)
 try: observed=metadata.version(name)
 except metadata.PackageNotFoundError: errors.append(f"MISSING {name}=={version}"); continue
 if observed!=version: errors.append(f"VERSION {name}: expected {version}, observed {observed}")
if errors: raise SystemExit("\n".join(errors))
print("Environment version check passed")
