#!/usr/bin/env python3
"""Configure the dedicated archive-52 inventory from v0.83.0's original metadata."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v0.83.0"
SOURCE = "01b189f6427601a15cbb3eb1563b5f82eabbafa3"
TREE = "b547eda9dd8f86db17c9a79093736eefbeeb9dc9"
TAG = "972dedddefe8a25286b9664b064ecfa6ad742c5f"
ZIP = "ee486739cef7bc1dc832c62aaecdfc85e02b0c9957cacdab1d6070a1a1cac451"
ZIP_BYTES = 590567603
TOOLING = "30530b3436a1a9737be93f67f308587f89b2f8bc"
EXTRACTOR = "38081b1791b49cb7328d18b4d4325c2876bb3bc8d7db03f4610f8d8a7c4bf91b"

def sha(data): return hashlib.sha256(data).hexdigest()
def json_bytes(value): return (json.dumps(value, indent=2) + "\n").encode()

def main():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import verify
    metadata = ROOT / "metadata" / VERSION
    record = json.loads((metadata / "release.json").read_bytes())
    manifest = json.loads((metadata / "manifest.json").read_bytes())
    checksum = (metadata / "distribution.zip.sha256").read_bytes()
    qualification = metadata / "source-qualification.json"
    assert record["version"] == manifest["version"] == VERSION
    assert record["sourceRevision"] == manifest["sourceRevision"] == SOURCE
    assert record["distributionSha256"] == ZIP == checksum.decode().split()[0]
    release = {
        "version": VERSION, "sourceRevision": SOURCE, "sourceTree": TREE, "tagObject": TAG,
        "distributionSha256": ZIP, "distributionBytes": ZIP_BYTES,
        "metadata": {name: sha((metadata / name).read_bytes()) for name in ("release.json", "manifest.json", "distribution.zip.sha256")},
        "sourceQualification": {"bytes": qualification.stat().st_size, "sha256": sha(qualification.read_bytes())},
    }
    lock = {
        "format": "revealline-archive-originals.v2", "archiveId": "archive-52", "repository": "mekhovov/revealline-archive-52",
        "sourceRepository": "mekhovov/revealline", "toolingCommit": TOOLING,
        "extractorPath": "publishing/pages-controller/extract-current.py", "extractorSha256": EXTRACTOR,
        "budgetBytes": 800000000, "releases": [release],
    }
    (ROOT / "source-lock.json").write_bytes(json_bytes(lock))
    rows = verify.metadata_inventory(ROOT, release)
    rows.extend([
        {"path": ".nojekyll", "bytes": 0, "sha256": sha(b"")},
        {"path": "index.html", "bytes": (ROOT / "index.html").stat().st_size, "sha256": sha((ROOT / "index.html").read_bytes())},
        {"path": "releases/index.html", "bytes": (ROOT / "releases/index.html").stat().st_size, "sha256": sha((ROOT / "releases/index.html").read_bytes())},
    ])
    rows.sort(key=lambda row: row["path"])
    inventory = {"base": "https://mekhovov.github.io/revealline-archive-52/", "files": rows}
    inventory_bytes = json_bytes(inventory)
    (ROOT / "expected-inventory.json").write_bytes(inventory_bytes)
    lock.update({"expectedInventorySha256": sha(inventory_bytes), "expectedFiles": len(rows), "expectedBytes": sum(row["bytes"] for row in rows)})
    (ROOT / "source-lock.json").write_bytes(json_bytes(lock))
    original = json.loads((ROOT / "authority/release-original.json").read_bytes())
    assert original["id"] == 394050785 and original["tag_name"] == VERSION
    assert not original["draft"] and not original["prerelease"]
    assert len(original["assets"]) == 9 and all(a["state"] == "uploaded" and a["digest"].startswith("sha256:") for a in original["assets"])
    assets = [{"id": a["id"], "name": a["name"], "bytes": a["size"], "sha256": a["digest"].removeprefix("sha256:")} for a in original["assets"]]
    assert next(a for a in assets if a["name"] == "distribution.zip")["sha256"] == ZIP
    assert next(a for a in assets if a["name"] == "distribution.zip")["bytes"] == ZIP_BYTES
    reviewed = json.loads((ROOT / "authority/reviewed-release-descriptors.json").read_bytes())
    assert len({a["name"] for a in assets}) == 9
    assert {a["name"]: (a["bytes"], a["sha256"]) for a in assets} == {a["name"]: (a["bytes"], a["sha256"]) for a in reviewed["artifacts"]}
    tag = json.loads((ROOT / "authority/tag-original.json").read_bytes())
    ref = json.loads((ROOT / "authority/tag-ref-original.json").read_bytes())
    assert tag["sha"] == ref["object"]["sha"] == TAG and tag["object"]["sha"] == SOURCE and tag["object"]["type"] == "commit"
    (ROOT / "input-authority.json").write_bytes(json_bytes({
        "version": VERSION, "releaseId": 394050785, "source": SOURCE, "tree": TREE, "tagObject": TAG,
        "donorCommit": "8bf0ed6c3947ca8c47ad2d9246db3e57acd986cf", "toolingCommit": TOOLING, "donorDeploymentMerge": None, "priorAcceptedPaths": 0,
        "mainPublisherRun": None, "archivePublicAcceptance": False,
        "releaseUrl": original["html_url"], "publishedAt": original["published_at"],
        "originalAssets": assets,
        "authorityFiles": {p.name: sha(p.read_bytes()) for p in sorted((ROOT / "authority").glob("*.json"))},
    }))

if __name__ == "__main__": main()
