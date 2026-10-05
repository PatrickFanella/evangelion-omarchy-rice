#!/usr/bin/env python3
"""Reproducibility and isolated lifecycle test for complete-suite archives."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd=None, env=None):
    result = subprocess.run(args, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise AssertionError(f"command failed ({result.returncode}): {' '.join(args)}\n{result.stdout}")
    return result


with tempfile.TemporaryDirectory(prefix="subcult-artifact-test-") as raw:
    tmp = Path(raw)
    clone = tmp / "source"
    shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "build", "test-results", "__pycache__", "*.pyc"))
    run("git", "init", "--quiet", cwd=clone)
    run("git", "add", ".", cwd=clone)
    run("git", "-c", "user.name=Artifact Test", "-c", "user.email=test@example.invalid",
        "commit", "--quiet", "-m", "artifact fixture", cwd=clone)
    run("git", "tag", "v0.0.0-ci.1", cwd=clone)
    out_a, out_b = tmp / "a", tmp / "b"
    run(str(clone / "scripts/build-release"), "build", "--tag", "v0.0.0-ci.1", "--output", str(out_a), cwd=clone)
    run(str(clone / "scripts/build-release"), "build", "--tag", "v0.0.0-ci.1", "--output", str(out_b), cwd=clone)
    archive_a = out_a / "subcult-omarchy-rice-0.0.0-ci.1.tar.gz"
    archive_b = out_b / archive_a.name
    assert archive_a.read_bytes() == archive_b.read_bytes(), "archive is not reproducible"
    run(str(clone / "scripts/build-release"), "verify", str(archive_a), cwd=clone)

    extract = tmp / "extract"
    extract.mkdir()
    with tarfile.open(archive_a, "r:gz") as tar:
        tar.extractall(extract, filter="data")
    suite = extract / "subcult-omarchy-rice-0.0.0-ci.1"
    files = {str(path.relative_to(suite)) for path in suite.rglob("*") if path.is_file()}
    for denied in (".git", ".github", ".gitea", "media", "release", "captures", "test-results", "packaging/gallery"):
        assert not any(path == denied or path.startswith(denied + "/") for path in files), denied

    provenance = json.loads((suite / "RELEASE-PROVENANCE.json").read_text())
    assert provenance["tag"] == "v0.0.0-ci.1" and len(provenance["commit"]) == 40
    assert provenance["publish"] is False

    home, state = tmp / "home", tmp / "state"
    home.mkdir(); state.mkdir()
    env = os.environ | {
        "HOME": str(home), "XDG_STATE_HOME": str(state),
        "SUBCULT_SKIP_ACTIVATE": "1", "SUBCULT_SOURCE_ONLY": "1",
        "SUBCULT_RELEASE_ARTIFACT_NESTED": "1",
    }
    run(str(suite / "preflight.py"), "--source-only", cwd=suite, env=env)
    run(str(suite / "scripts/build-release"), "verify-root", str(suite), cwd=suite, env=env)
    run(str(suite / "install.sh"), "--dry-run", "--preset", "minimal", cwd=suite, env=env)
    first = run(str(suite / "install.sh"), "--apply", "--yes", "--preset", "minimal", cwd=suite, env=env)
    first_snapshot = Path(first.stdout.strip().split("rollback snapshot: ")[-1])
    assert first_snapshot.is_dir()
    second = run(str(suite / "install.sh"), "--apply", "--yes", "--preset", "minimal", cwd=suite, env=env)
    second_snapshot = Path(second.stdout.strip().split("rollback snapshot: ")[-1])
    run(str(suite / "rollback.sh"), str(second_snapshot), cwd=suite, env=env)
    run(str(suite / "rollback.sh"), str(first_snapshot), cwd=suite, env=env)
    theme_root = home / ".config/omarchy/themes/subcult"
    assert not theme_root.exists() or not any(path.is_file() for path in theme_root.rglob("*")), \
        "rollback/removal left owned theme payload"

    report = {
        "schema_version": 1,
        "status": "passed",
        "tag": provenance["tag"],
        "commit": provenance["commit"],
        "archive_sha256": hashlib.sha256(archive_a.read_bytes()).hexdigest(),
        "checks": ["exact-tag", "allowlist", "reproducible", "external-checksum",
                   "internal-manifest", "offline-preflight", "dry-run", "install",
                   "upgrade", "rollback", "removal", "no-publication"],
    }
    output = Path(os.environ.get("SUBCULT_RELEASE_ARTIFACT_REPORT", ROOT / "test-results/release-artifact.json"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")

print("PASS  reproducible exact-tag release artifact and offline lifecycle")
