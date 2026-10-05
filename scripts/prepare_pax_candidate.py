"""Prepare the exact published Pax proposal in a clean disposable source checkout."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from typing import TypedDict

from prepare_candidate import git, read_patch, require_list, require_object, require_string


BASE = "2f62f678d06f8444ddc7788ce03e1f1f46cf4cba"
PATCH_FILE = "proposals/pax-eligibility-validation.patch"
PATCH_SHA256 = "93045a70721ebce5162e9cdd873ee1b30d94abbfd10dca243957e5bac462f03a"
ORIGIN = "https://github.com/Bridge-Node-7/pax-silica"
CHANGED_FILES = ("scripts/validate_data.py", "tests/test_snapshot_boundary.py")
DATA_FILES = (
    "data/evidence-baseline.json", "data/pax-silica.json",
    "data/schemas/pax-silica.schema.json", "data/schemas/sources.schema.json",
    "data/sources.json",
)
PUBLIC_FILES = ("app.js", "data/pax-silica.json", "data/sources.json", "index.html", "styles.css")
REVIEW_FILES = (
    ".github/workflows/pax-candidate-verification.yml", "scripts/prepare_candidate.py",
    "scripts/prepare_pax_candidate.py", "scripts/collect_pax_results.py",
    "scripts/collect_codeql.py", "scripts/collect_pax_codeql.py",
)
RUNNER_KEYS = (
    "RUNNER_OS", "RUNNER_ARCH", "RUNNER_TEMP", "ImageOS", "ImageVersion",
    "GITHUB_REPOSITORY", "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_JOB", "GITHUB_SHA",
)


class BuildRecord(TypedDict):
    command: list[str]
    exit_code: int
    raw_local_log: str
    raw_local_log_sha256: str
    files_sha256: dict[str, str]
    manifest_entries_verified: int


def sha256(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Expected a regular file for hashing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_hashes(value: object, context: str) -> dict[str, str]:
    record = require_object(value, context)
    hashes = {name: require_string(digest, f"{context}.{name}") for name, digest in record.items()}
    for name, digest in hashes.items():
        if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise ValueError(f"Invalid SHA256 for {context}.{name}: {digest}")
    return hashes


def require_external(source: Path, path: Path) -> None:
    if path.is_relative_to(source) or source.is_relative_to(path):
        raise ValueError(f"Path must be separate from the disposable source checkout {source}: {path}")


def require_clean_source(source: Path) -> None:
    status = git(source, ["status", "--porcelain", "--untracked-files=all"])
    ignored = git(source, ["ls-files", "--others", "--ignored", "--exclude-standard"])
    if status or ignored:
        raise ValueError(f"Disposable source must have no changed, untracked or ignored files: status={status!r}; ignored={ignored!r}")


def tracked_hash(root: Path, revision: str, relative: str) -> str:
    command = ["git", "--no-pager", "show", f"{revision}:{relative}"]
    try:
        result = subprocess.run(command, cwd=root, check=True, capture_output=True)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"Could not read tracked bytes in {root}: {command}; exit={error.returncode}; "
            f"stderr={error.stderr.decode('utf-8', errors='replace')}"
        ) from error
    observed = sha256(root / relative)
    committed = hashlib.sha256(result.stdout).hexdigest()
    if observed != committed:
        raise ValueError(f"Working file bytes differ from {revision}:{relative}: {observed} != {committed}")
    return observed


def require_review(review: Path) -> str:
    if Path(git(review, ["rev-parse", "--show-toplevel"])).resolve() != review:
        raise ValueError(f"Review path must be its Git checkout root: {review}")
    status = git(review, ["status", "--porcelain", "--untracked-files=all"])
    if status:
        raise ValueError(f"Review checkout must be clean at the executed commit: {status}")
    commit = git(review, ["rev-parse", "HEAD"])
    executed = require_string(os.environ["GITHUB_SHA"], "GITHUB_SHA")
    if executed != commit:
        raise ValueError(f"Executed review SHA {executed} differs from review HEAD {commit}")
    return commit


def published_patch(review: Path) -> Path:
    document = require_object(json.loads((review / "evidence/verification.json").read_text(encoding="utf-8")), "verification")
    records = [read_patch(item) for item in require_list(document["candidate_patches"], "candidate_patches")]
    matches = [record for record in records if record["file"] == PATCH_FILE]
    if len(matches) != 1:
        raise ValueError(f"Expected one published Pax patch record; found {len(matches)}")
    record = matches[0]
    if record["repository"] != "pax-silica" or record["base_sha"] != BASE or record["sha256"] != PATCH_SHA256:
        raise ValueError(f"Published Pax provenance differs from the approved repository/base/patch: {record}")
    path = (review / PATCH_FILE).resolve()
    if not path.is_relative_to(review / "proposals") or sha256(path) != PATCH_SHA256:
        raise ValueError(f"Published Pax patch bytes do not match {PATCH_SHA256}: {path}")
    return path


def data_hashes(source: Path) -> dict[str, str]:
    observed = tuple(sorted(path.relative_to(source).as_posix() for path in (source / "data").rglob("*") if path.is_file()))
    if observed != DATA_FILES:
        raise ValueError(f"Expected exactly five canonical Pax data files; found {observed}")
    return {relative: sha256(source / relative) for relative in DATA_FILES}


def public_build_hashes(build: Path) -> dict[str, str]:
    expected = set(PUBLIC_FILES) | {"WEB_MANIFEST.sha256"}
    paths = tuple(build.rglob("*"))
    if any(path.is_symlink() for path in paths):
        raise ValueError(f"Public build contains a symlink: {build}")
    observed = {path.relative_to(build).as_posix() for path in paths if path.is_file()}
    if observed != expected:
        raise ValueError(f"Public build {build} must contain exactly six files: {sorted(observed)}")
    entries = (build / "WEB_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    parsed: list[tuple[str, str]] = []
    for line in entries:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            raise ValueError(f"Malformed WEB_MANIFEST entry in {build}: {line!r}")
        parsed.append((match[1], match[2]))
    if tuple(relative for _, relative in parsed) != PUBLIC_FILES:
        raise ValueError(f"WEB_MANIFEST must identify the five expected payload files once in canonical order: {parsed}")
    hashes = {relative: sha256(build / relative) for relative in sorted(expected)}
    for digest, relative in parsed:
        if hashes[relative] != digest:
            raise ValueError(f"WEB_MANIFEST hash mismatch for {build / relative}: {digest} != {hashes[relative]}")
    return hashes


def generate_build(source: Path, output: Path) -> BuildRecord:
    require_external(source, output)
    log = output.with_name(output.name + ".log")
    if output.exists() or log.exists():
        raise FileExistsError(f"Refusing to overwrite existing public build or log: {output}; {log}")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, str(source / "scripts/build_web.py"), "--output", str(output)]
    with log.open("xb") as stream:
        result = subprocess.run(command, cwd=source, stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        raise RuntimeError(f"Public build failed: command={command}; exit={result.returncode}; raw_log={log}")
    return {
        "command": command, "exit_code": result.returncode, "raw_local_log": log.name,
        "raw_local_log_sha256": sha256(log), "files_sha256": public_build_hashes(output),
        "manifest_entries_verified": len(PUBLIC_FILES),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--baseline-build", type=Path, required=True)
    args = parser.parse_args()
    source: Path = args.source.resolve()
    review: Path = args.review.resolve()
    evidence: Path = args.evidence.resolve()
    baseline: Path = args.baseline_build.resolve()
    for path in (review, evidence, baseline, Path(sys.prefix).resolve()):
        require_external(source, path)
    if baseline.is_relative_to(evidence) or evidence.is_relative_to(baseline):
        raise ValueError("Baseline build must be outside the bounded artifact directory")
    if (evidence / "preparation.json").exists():
        raise FileExistsError(f"Refusing to overwrite retained preparation: {evidence}")
    missing = [key for key in RUNNER_KEYS if not os.environ.get(key)]
    if missing:
        raise ValueError(f"Required runner provenance fields are missing: {missing}")
    if os.environ["GITHUB_REPOSITORY"] != "hideouts-io/bridgenode7-technical-review":
        raise ValueError(f"Unexpected executing review repository: {os.environ['GITHUB_REPOSITORY']}")
    if sys.version_info[:2] not in {(3, 11), (3, 12)}:
        raise ValueError(f"Pax verification requires declared Python 3.11 or 3.12; selected {platform.python_version()}")
    review_commit = require_review(review)
    review_hashes = {relative: tracked_hash(review, review_commit, relative) for relative in REVIEW_FILES}
    patch = published_patch(review)
    tracked_hash(review, review_commit, PATCH_FILE)
    tracked_hash(review, review_commit, "evidence/verification.json")
    if Path(git(source, ["rev-parse", "--show-toplevel"])).resolve() != source:
        raise ValueError(f"Source path must be its Git checkout root: {source}")
    if git(source, ["rev-parse", "HEAD"]) != BASE:
        raise ValueError(f"Pax source HEAD must be the published base {BASE}")
    if git(source, ["remote", "get-url", "origin"]).removesuffix(".git") != ORIGIN:
        raise ValueError(f"Pax source origin must be {ORIGIN}")
    require_clean_source(source)
    numstat = git(source, ["apply", "--numstat", str(patch)]).splitlines()
    if tuple(sorted(line.split("\t", 2)[2] for line in numstat)) != CHANGED_FILES:
        raise ValueError(f"Pax patch must modify only the validator and snapshot tests: {numstat}")
    git(source, ["apply", "--check", "--whitespace=error-all", str(patch)])
    canonical = data_hashes(source)
    workflows = {
        path.name: tracked_hash(source, BASE, path.relative_to(source).as_posix())
        for path in sorted((source / ".github/workflows").iterdir()) if path.suffix in {".yml", ".yaml"}
    }
    baseline_record = generate_build(source, baseline)
    require_clean_source(source)
    if data_hashes(source) != canonical:
        raise ValueError("Baseline generation changed canonical Pax data")
    git(source, ["apply", "--index", "--whitespace=error-all", str(patch)])
    changed = git(source, ["diff", "--cached", "--name-status"]).splitlines()
    if changed != [f"M\t{relative}" for relative in CHANGED_FILES]:
        raise ValueError(f"Unexpected staged Pax changes: {changed}")
    git(source, ["diff", "--cached", "--check"])
    git(source, ["-c", "user.name=Independent review candidate", "-c", "user.email=review@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-m", "Temporary Pax candidate for independent validation"])
    require_clean_source(source)
    if data_hashes(source) != canonical:
        raise ValueError("Candidate preparation changed canonical Pax data")
    provenance = {
        "scope": "Pax-only candidate verification; no upstream publication or deployment",
        "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": "Bridge-Node-7/pax-silica", "origin": ORIGIN, "upstream_base": BASE,
        "patch": {"file": PATCH_FILE, "sha256": PATCH_SHA256},
        "temporary_candidate_commit": git(source, ["rev-parse", "HEAD"]), "temporary_commit_pushed": False,
        "changed_files": list(CHANGED_FILES),
        "changed_files_sha256": {relative: sha256(source / relative) for relative in CHANGED_FILES},
        "canonical_data_sha256": canonical, "source_workflows_sha256": workflows,
        "baseline_build": baseline_record, "review_commit": review_commit,
        "executed_review_sha": os.environ["GITHUB_SHA"], "review_files_sha256": review_hashes,
        "review_workflow_sha256": review_hashes[REVIEW_FILES[0]],
        "runtime": {"python": platform.python_version(), "executable": sys.executable,
                    "prefix": sys.prefix, "platform": platform.platform(), "machine": platform.machine()},
        "runner": {key: os.environ[key] for key in RUNNER_KEYS},
    }
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "preparation.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
