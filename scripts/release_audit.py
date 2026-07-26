from __future__ import annotations
import csv, json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors, warnings = [], []
ignore_parts = {".git", "__pycache__", ".pytest_cache", ".venv"}
excluded_names = {"MANIFEST.csv", "SOURCE_SHA256SUMS.txt", "OUTPUT_SHA256SUMS.txt"}
files = [p for p in ROOT.rglob("*") if p.is_file() and not any(x in ignore_parts for x in p.parts) and p.name not in excluded_names and p.relative_to(ROOT).as_posix() != "outputs/reports/release_audit.json"]

workflow_debris = [
    r"(?:^|[/_.-])rc\d+(?:$|[/_.-])",
    r"conditional",
    r"final[_ -]?candidate",
    r"handover",
    r"operator[_ -]?note",
    r"conversation[_ -]?export",
    r"prompt[_ -]?file",
]
for p in files:
    rel = p.relative_to(ROOT).as_posix()
    low = rel.lower()
    if p.suffix.lower() in {".zip", ".7z", ".rar"}:
        errors.append(f"nested archive: {rel}")
    if any(re.search(pattern, low) for pattern in workflow_debris):
        errors.append(f"workflow-specific file name: {rel}")
    if any(part.lower() in {"controlled", "restricted", "raw", "private"} for part in p.parts):
        errors.append(f"non-public directory in release tree: {rel}")

    if p.suffix.lower() == ".csv" and "data/aggregate/" in rel:
        with p.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        if len(rows) > 101:
            errors.append(f"aggregate CSV exceeds row ceiling: {rel} ({len(rows)-1} rows)")
        header = [h.strip().lower() for h in (rows[0] if rows else [])]
        sensitive = {"case_id", "response_id", "ipaddr", "ip_address", "submitdate", "startdate", "datestamp", "seed", "token", "email", "phone", "free_text"}
        hits = sorted(set(header) & sensitive)
        if hits:
            errors.append(f"sensitive aggregate headers in {rel}: {hits}")

    if p.suffix.lower() == ".docx":
        with zipfile.ZipFile(p) as zf:
            names = set(zf.namelist())
            for forbidden_part in ["word/comments.xml", "word/people.xml"]:
                if forbidden_part in names:
                    errors.append(f"hidden Word review part in {rel}: {forbidden_part}")
            xml = "".join(zf.read(n).decode("utf-8", errors="ignore") for n in names if n.endswith(".xml"))
            if re.search(r"<w:(?:ins|del|commentRangeStart|commentReference)\b", xml):
                errors.append(f"tracked revision or comment marker in {rel}")

    if p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".woff", ".ttf", ".docx"}:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)", txt):
            errors.append(f"IPv4-like value: {rel}")
        if p.name not in {"release_audit.py", "test_release_integrity.py"}:
            if re.search(r"/(?:mnt/data|home/oai)/|[A-Za-z]:\\(?:Users|Temp|Windows|Program Files)", txt):
                errors.append(f"local path: {rel}")
            if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|github_pat_|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}", txt):
                errors.append(f"secret pattern: {rel}")
            machine_provenance_phrases = [
                "generated" + " by " + "chat" + "gpt",
                "generated" + " using " + "open" + "ai",
                "as an " + "ai" + " language model",
            ]
            for phrase in machine_provenance_phrases + ["todo", "fixme", "tbd", "placeholder text"]:
                if phrase in txt.lower():
                    errors.append(f"unresolved or machine-provenance phrase in {rel}")

# Public data layout is fail-closed.
data_root = ROOT / "data"
actual_data_files = sorted(p.relative_to(ROOT).as_posix() for p in data_root.rglob("*") if p.is_file())
if not actual_data_files or not all(x.startswith("data/aggregate/") for x in actual_data_files):
    errors.append("public data tree contains a non-aggregate path")
for name in ["responses", "respondent", "free_text_review_register", "results-survey", "survey_444639"]:
    if any(name in p.relative_to(ROOT).as_posix().lower() for p in files):
        errors.append(f"response-level or raw-source filename token present: {name}")

metadata = json.loads((ROOT / "metadata" / "release_metadata.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "metadata" / "release_scope.json").read_text(encoding="utf-8"))
if metadata["software"]["version"] != (ROOT / "VERSION").read_text(encoding="utf-8").strip():
    errors.append("version mismatch between release metadata and VERSION")
if metadata["release"]["doi"] != "10.5281/zenodo.21603732":
    errors.append("reserved version DOI is not integrated")
if metadata["release"].get("previous_version_doi") != "10.5281/zenodo.21586875":
    errors.append("previous version DOI is not integrated")
if scope.get("row_level_data_present") is not False:
    errors.append("release scope does not assert row_level_data_present=false")

workflow = (ROOT / ".github" / "workflows" / "reproducibility.yml").read_text(encoding="utf-8")
uses = re.findall(r"uses:\s*([^\s#]+)", workflow)
for use in uses:
    if "@" not in use or not re.fullmatch(r"[^@]+@[0-9a-f]{40}", use):
        errors.append(f"GitHub Action is not pinned to a full SHA: {use}")
if "permissions:\n  contents: read" not in workflow:
    errors.append("workflow least-privilege permission missing")
if "pull_request_target" in workflow:
    errors.append("pull_request_target is forbidden")

status = "PASS" if not errors else "FAIL"
report = {
    "status": status,
    "files_scanned": len(files),
    "errors": errors,
    "warnings": warnings,
    "row_level_data_present": False,
    "doi": metadata["release"]["doi"],
}
path = ROOT / "outputs" / "reports" / "release_audit.json"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, sort_keys=True))
if errors:
    raise SystemExit(1)
