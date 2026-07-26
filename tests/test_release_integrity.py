from __future__ import annotations
import json, re, subprocess, sys, zipfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_version_doi_and_repository_metadata():
    metadata = json.loads((ROOT / "metadata/release_metadata.json").read_text(encoding="utf-8"))
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "2.0.2" == metadata["software"]["version"]
    assert metadata["software"]["repository_url"] == "https://github.com/antonioclim/ai-romania-sme-digital-restructuring"
    assert metadata["release"]["doi"] == "10.5281/zenodo.21603732"
    assert metadata["release"]["previous_version_doi"] == "10.5281/zenodo.21586875"


def test_generated_metadata_is_current():
    result = subprocess.run([sys.executable, "scripts/generate_metadata.py", "--check"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert citation["doi"] == "10.5281/zenodo.21603732"
    codemeta = json.loads((ROOT / "codemeta.json").read_text(encoding="utf-8"))
    assert codemeta["identifier"] == "https://doi.org/10.5281/zenodo.21603732"
    zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    assert zenodo["access_right"] == "open" and zenodo["version"] == "2.0.2"


def test_action_pins_and_permissions():
    workflow = (ROOT / ".github/workflows/reproducibility.yml").read_text(encoding="utf-8")
    assert "actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert not re.search(r"uses:\s*[^\s#]+@v\d", workflow)
    assert "permissions:\n  contents: read" in workflow
    assert "MPLCONFIGDIR: /tmp/matplotlib" in workflow
    assert "${{ runner.temp }}" not in workflow


def test_pyyaml_dependency_is_declared_consistently():
    assert "pyyaml==6.0.3" in (ROOT / "requirements.lock.txt").read_text(encoding="utf-8").lower()
    assert "pyyaml==6.0.3" in (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
    assert "pyyaml==6.0.3" in (ROOT / "environment.yml").read_text(encoding="utf-8").lower()


def test_questionnaire_documents_are_clean():
    docs = list((ROOT / "survey").glob("*.docx"))
    assert len(docs) == 2
    for path in docs:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            assert "word/comments.xml" not in names
            xml = "".join(zf.read(n).decode("utf-8", errors="ignore") for n in names if n.endswith(".xml"))
            assert not re.search(r"<w:(?:ins|del|commentRangeStart|commentReference)\b", xml)


def test_survey_documentation_is_present():
    required = [
        "DESCRIPTIONS.md", "questionnaire_ro.md", "questionnaire_en.md",
        "questionnaire_ro.pdf", "questionnaire_en.pdf", "questionnaire_ro.docx",
        "questionnaire_en.docx", "questionnaire_items.csv", "response_options.csv",
        "variable_dictionary.csv", "instrument_model.json", "response_coding_guide.md",
        "translation_and_semantic_review_protocol.md", "source_wording_fidelity.md",
    ]
    for name in required:
        assert (ROOT / "survey" / name).exists(), name


def test_public_release_has_no_response_rows():
    data_files = [p for p in (ROOT / "data").rglob("*") if p.is_file()]
    assert data_files and all("aggregate" in p.parts for p in data_files)
    for path in data_files:
        lines = path.read_text(encoding="utf-8-sig", errors="ignore").splitlines()
        assert len(lines) <= 101, (path, len(lines) - 1)
        if lines:
            header = lines[0].lower()
            for token in ["case_id", "response_id", "ipaddr", "submitdate", "startdate", "datestamp", "seed", "token", "free_text"]:
                assert token not in header, (path, token)


def test_release_audit_passes():
    result = subprocess.run([sys.executable, "scripts/release_audit.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((ROOT / "outputs/reports/release_audit.json").read_text(encoding="utf-8"))
    assert report["status"] == "PASS"


def test_manifest_check_passes():
    result = subprocess.run([sys.executable, "scripts/generate_manifests.py", "--check"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
