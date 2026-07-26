from __future__ import annotations
import argparse,csv,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={"SOURCE_SHA256SUMS.txt","OUTPUT_SHA256SUMS.txt","MANIFEST.csv"}
IGNORE_PARTS={".git","__pycache__",".pytest_cache",".venv"}

def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()

def source_files():
 return [p for p in sorted(ROOT.rglob("*")) if p.is_file() and not any(x in IGNORE_PARTS for x in p.parts) and "outputs" not in p.parts and p.name not in EXCLUDE and p.suffix!=".pyc"]

def all_files():
 return [p for p in sorted(ROOT.rglob("*")) if p.is_file() and not any(x in IGNORE_PARTS for x in p.parts) and p.name not in EXCLUDE and p.suffix!=".pyc"]

def sums(files): return "".join(f"{sha(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in files)
def manifest(files):
 rows=[{"path":p.relative_to(ROOT).as_posix(),"size_bytes":p.stat().st_size,"sha256":sha(p)} for p in files]
 out=["path,size_bytes,sha256"]+[f"{r['path']},{r['size_bytes']},{r['sha256']}" for r in rows]
 return "\n".join(out)+"\n"
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--write",action="store_true"); ap.add_argument("--check",action="store_true"); a=ap.parse_args()
 expected_source=sums(source_files()); expected_manifest=manifest(all_files()); errors=[]
 if a.write:
  (ROOT/"SOURCE_SHA256SUMS.txt").write_text(expected_source,encoding="utf-8",newline="\n")
  (ROOT/"MANIFEST.csv").write_text(expected_manifest,encoding="utf-8",newline="\n")
 if a.check:
  if not (ROOT/"SOURCE_SHA256SUMS.txt").exists() or (ROOT/"SOURCE_SHA256SUMS.txt").read_text(encoding="utf-8")!=expected_source: errors.append("SOURCE_SHA256SUMS.txt")
  if not (ROOT/"MANIFEST.csv").exists() or (ROOT/"MANIFEST.csv").read_text(encoding="utf-8")!=expected_manifest: errors.append("MANIFEST.csv")
 if errors: raise SystemExit("Manifest mismatch: "+", ".join(errors))
 print("Source/full manifest generation/check passed")
if __name__=="__main__": main()
