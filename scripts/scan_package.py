from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
patterns = [
    r"\bcase_id\b",
    r"\bresponse_id\b",
    r"\bipaddr\b",
    r"\bsubmitdate\b",
    r"\bstartdate\b",
    r"\bdatestamp\b",
    r"results-survey",
    r"survey_444639",
    r"editorialmanager",
    r"\.7z",
]
hits = []
for p in ROOT.rglob("*"):
    if not p.is_file() or any(x in p.parts for x in [".git", ".venv", "__pycache__", ".pytest_cache"]):
        continue
    if p.name in {"scan_package.py", "release_audit.py", "test_release_integrity.py", ".gitignore"} or "tests" in p.parts:
        continue
    rel = p.relative_to(ROOT).as_posix()
    # The variable dictionary legitimately names excluded administrative source fields
    # as documentary metadata. It contains no respondent values and is checked by the
    # release audit separately, so lexical matches there are not disclosure events.
    if rel == "survey/variable_dictionary.csv":
        continue
    if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".zip", ".docx", ".pyc"}:
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    for pattern in patterns:
        if re.search(pattern, text, re.I):
            hits.append({"path": p.relative_to(ROOT).as_posix(), "pattern": pattern})
status = "PASS" if not hits else "FAIL"
print(json.dumps({"status": status, "hits": hits}, indent=2))
if hits:
    raise SystemExit(1)
