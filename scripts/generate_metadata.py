from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "metadata" / "release_metadata.json"


def render(master):
    s = master["software"]
    a = master["author"]
    r = master["release"]
    cff = [
        "cff-version: 1.2.0",
        f'title: "{s["title"]}"',
        'message: "If you use this software, cite the versioned software release. Cite the associated article separately when available."',
        "type: software",
        "authors:",
        f'  - family-names: {a["family_name"]}',
        f'    given-names: {a["given_name"]}',
        f'    affiliation: "{a["affiliation"]}"',
        f'version: "{s["version"]}"',
        f'doi: "{r["doi"]}"',
        f'url: "https://doi.org/{r["doi"]}"',
        f'repository-code: "{s["repository_url"]}"',
        f'license: {s["license"]}',
        "keywords:",
        *[f"  - {k}" for k in s["keywords"]],
    ]
    codemeta = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode",
        "name": s["title"],
        "version": s["version"],
        "description": s["description"],
        "identifier": "https://doi.org/" + r["doi"],
        "sameAs": "https://doi.org/" + r["doi"],
        "codeRepository": s["repository_url"],
        "issueTracker": s["repository_url"] + "/issues",
        "programmingLanguage": "Python",
        "runtimePlatform": "Python 3.13",
        "license": "https://spdx.org/licenses/MIT",
        "author": [{
            "@type": "Person",
            "givenName": a["given_name"],
            "familyName": a["family_name"],
            "affiliation": {"@type": "Organization", "name": a["affiliation"]},
        }],
        "keywords": s["keywords"],
    }
    zenodo = {
        "title": s["title"],
        "upload_type": "software",
        "version": s["version"],
        "creators": [{
            "name": f'{a["family_name"]}, {a["given_name"]}',
            "affiliation": a["affiliation"],
        }],
        "license": s["license"],
        "access_right": "open",
        "description": s["description"],
        "keywords": s["keywords"],
    }
    return {
        "CITATION.cff": "\n".join(cff) + "\n",
        "codemeta.json": json.dumps(codemeta, indent=2, sort_keys=True) + "\n",
        ".zenodo.json": json.dumps(zenodo, indent=2, sort_keys=True) + "\n",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    rendered = render(master)
    errors = []
    for rel, content in rendered.items():
        path = ROOT / rel
        if args.write:
            path.write_text(content, encoding="utf-8", newline="\n")
        if args.check and (not path.exists() or path.read_text(encoding="utf-8") != content):
            errors.append(rel)
    if errors:
        raise SystemExit("Metadata mismatch: " + ", ".join(errors))
    print("Metadata generation/check passed")


if __name__ == "__main__":
    main()
