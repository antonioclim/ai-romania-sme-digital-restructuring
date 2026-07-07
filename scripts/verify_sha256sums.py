from __future__ import annotations
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    manifest = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'SHA256SUMS.txt')
    if not manifest.exists():
        print(f'MISSING manifest: {manifest.relative_to(ROOT)}')
        raise SystemExit(1)

    ok = True
    for line_no, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            print(f'FAIL line {line_no}: malformed checksum entry')
            ok = False
            continue
        expected, rel = parts
        rel = rel.lstrip('*')
        path = ROOT / rel
        if not path.exists():
            print(f'MISSING  {rel}')
            ok = False
            continue
        observed = sha256(path)
        if observed == expected:
            print(f'OK  {rel}')
        else:
            print(f'FAIL  {rel}')
            print(f'      expected: {expected}')
            print(f'      observed: {observed}')
            ok = False
    if not ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
