from __future__ import annotations
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def verify(path):
 errors=[]
 for line in path.read_text(encoding="utf-8").splitlines():
  if not line.strip(): continue
  expected,rel=line.split("  ",1); p=ROOT/rel
  if not p.exists(): errors.append(f"MISSING {rel}")
  elif sha(p)!=expected: errors.append(f"MISMATCH {rel}")
 if errors: raise SystemExit("\n".join(errors))
 print(f"Checksum verification passed: {path.name}")
if __name__=="__main__":
 ap=argparse.ArgumentParser(); ap.add_argument("--scope",choices=["source","outputs"]); a=ap.parse_args(); verify(ROOT/("SOURCE_SHA256SUMS.txt" if a.scope=="source" else "OUTPUT_SHA256SUMS.txt"))
