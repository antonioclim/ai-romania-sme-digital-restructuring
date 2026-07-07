from __future__ import annotations
import hashlib, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    manifest = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'SHA256SUMS.txt')
    ok = True
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        expected, rel = line.split(maxsplit=1)
        rel = rel.lstrip('*')
        path = ROOT / rel
        observed = sha256(path)
        status = 'OK' if observed == expected else 'FAIL'
        print(f'{status}  {rel}')
        if status != 'OK':
            ok = False
    if not ok:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
