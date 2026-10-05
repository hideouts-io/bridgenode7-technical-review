"""Verify and apply published patches in an otherwise clean disposable checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
from typing import TypedDict, cast


class Patch(TypedDict):
    file: str
    repository: str
    base_sha: str
    sha256: str


def require_object(value: object, context: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise TypeError(f"{context} must be an object with string keys")
    return cast(dict[str, object], value)


def require_list(value: object, context: str) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"{context} must be an array")
    return cast(list[object], value)


def require_string(value: object, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{context} must be a nonempty string")
    return value


def read_patch(value: object) -> Patch:
    record = require_object(value, "candidate patch")
    patch: Patch = {
        "file": require_string(record["file"], "patch.file"),
        "repository": require_string(record["repository"], "patch.repository"),
        "base_sha": require_string(record["base_sha"], "patch.base_sha"),
        "sha256": require_string(record["sha256"], "patch.sha256"),
    }
    if re.fullmatch(r"[0-9a-f]{40}", patch["base_sha"]) is None:
        raise ValueError(f"Invalid source commit: {patch['base_sha']}")
    if re.fullmatch(r"[0-9a-f]{64}", patch["sha256"]) is None:
        raise ValueError(f"Invalid patch hash: {patch['file']}")
    return patch


def git(source: Path, arguments: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", "--no-pager", *arguments], cwd=source,
            check=True, text=True, encoding="utf-8", capture_output=True,
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"Git failed in {source}: {error.cmd}; exit={error.returncode}; "
            f"stdout={error.stdout}; stderr={error.stderr}"
        ) from error
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--patch", action="append", required=True)
    args = parser.parse_args()
    source: Path = args.source.resolve()
    review: Path = args.review.resolve()
    evidence: Path = args.evidence.resolve()
    requested: list[str] = args.patch
    document = require_object(json.loads((review / "evidence/verification.json").read_text()), "verification")
    published = [read_patch(item) for item in require_list(document["candidate_patches"], "candidate_patches")]
    selected: list[Patch] = []
    for name in requested:
        matches = [patch for patch in published if patch["file"] == name]
        if len(matches) != 1:
            raise ValueError(f"Expected one published patch record for {name}; found {len(matches)}")
        selected.append(matches[0])
    if len(set(requested)) != len(requested):
        raise ValueError("Each patch must be supplied exactly once")
    repository = selected[0]["repository"]
    base = selected[0]["base_sha"]
    if repository not in {"materials-to-mission", "frontier-decision-engine", "ai-cyber-assurance"}:
        raise ValueError(f"Repository outside hosted verification scope: {repository}")
    if any(patch["repository"] != repository or patch["base_sha"] != base for patch in selected):
        raise ValueError("Selected patches do not share a repository and source base")
    if evidence.is_relative_to(source) or review == source:
        raise ValueError("Evidence and review checkout must be outside the disposable source checkout")
    if git(source, ["rev-parse", "HEAD"]) != base:
        raise ValueError(f"Source HEAD does not match the published base {base}")
    expected_origin = f"https://github.com/Bridge-Node-7/{repository}"
    if git(source, ["remote", "get-url", "origin"]).removesuffix(".git") != expected_origin:
        raise ValueError(f"Source origin must be {expected_origin}")
    if git(source, ["status", "--porcelain"]):
        raise ValueError("Disposable source checkout must be clean before applying patches")
    paths: list[str] = []
    for patch in selected:
        path = (review / patch["file"]).resolve()
        if not path.is_relative_to(review / "proposals"):
            raise ValueError(f"Patch is outside the proposals directory: {patch['file']}")
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if observed != patch["sha256"]:
            raise ValueError(f"Patch hash mismatch for {patch['file']}: {observed}")
        paths.append(str(path))
    git(source, ["apply", "--check", "--whitespace=error-all", *paths])
    git(source, ["apply", "--index", "--whitespace=error-all", *paths])
    changed_files = git(source, ["diff", "--cached", "--name-only"]).splitlines()
    git(source, ["-c", "user.name=Independent review candidate", "-c", "user.email=review@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-m", "Temporary candidate for independent hosted validation"])
    if git(source, ["status", "--porcelain"]):
        raise ValueError("Candidate preparation left unexpected source changes")
    evidence.mkdir(parents=True, exist_ok=True)
    provenance = {
        "scope": "hosted candidate verification in the review repository",
        "repository": f"Bridge-Node-7/{repository}", "upstream_base": base,
        "patches": selected, "temporary_candidate_commit": git(source, ["rev-parse", "HEAD"]),
        "temporary_commit_pushed": False, "changed_files": changed_files,
        "source_workflows_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted((source / ".github/workflows").glob("*.yml"))
        },
        "review_commit": git(review, ["rev-parse", "HEAD"]),
        "review_workflow_sha256": hashlib.sha256((review / ".github/workflows/candidate-verification.yml").read_bytes()).hexdigest(),
        "python": platform.python_version(), "platform": platform.platform(),
        "runner": {key: os.environ[key] for key in (
            "RUNNER_OS", "RUNNER_ARCH", "ImageOS", "ImageVersion", "GITHUB_REPOSITORY",
            "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_JOB", "GITHUB_SHA",
        )},
    }
    (evidence / "preparation.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
