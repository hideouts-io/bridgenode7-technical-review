"""Verify real Pax gate output, unchanged data and byte-identical external builds."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import TypedDict

from prepare_candidate import git, require_object, require_string
from prepare_pax_candidate import (
    BASE, CHANGED_FILES, ORIGIN, PATCH_FILE, PATCH_SHA256, PUBLIC_FILES, REVIEW_FILES,
    data_hashes, generate_build, public_build_hashes, published_patch, read_hashes,
    require_clean_source, require_external, require_review, sha256, tracked_hash,
)


class GateRecord(TypedDict):
    tests: int
    duration_seconds: str
    unittest_outcome: str
    full_gate_flags: list[str]
    raw_local_log: str
    raw_local_log_sha256: str


def collect_gate(log: Path, version: str) -> GateRecord:
    text = log.read_text(encoding="utf-8")
    runs = re.findall(r"^Ran ([0-9]+) tests in ([0-9]+(?:\.[0-9]+)?)s$", text, re.MULTILINE)
    if len(runs) != 1 or int(runs[0][0]) < 1:
        raise ValueError(f"Expected one positive executed unittest count in {log}; found {runs}")
    lines = text.splitlines()
    if lines.count("OK") != 1 or re.search(r"^(?:FAILED|ERROR:|FAIL:|Traceback|FAIL -)", text, re.MULTILINE):
        raise ValueError(f"Pax unittest/full-gate output does not identify an unqualified success: {log}")
    flags = (
        f"PASS - release identity v{version}", "PASS - data integrity", "PASS - source credibility",
        "PASS - public boundary", "PASS - spoken-language audit", "PASS - rendered evidence taxonomy",
        "PASS - deterministic build", "PASS - evidence integrity", "PASS - generated public boundary",
        "PASS - tests", "PASS - repository gate",
    )
    missing = [flag for flag in flags if flag not in lines]
    if missing:
        raise ValueError(f"Pax complete-gate success flags missing from {log}: {missing}")
    for prefix in ("PASS - freshness as of ", "PASS - evidence source ratchet (",
                   "PASS - public source coverage (", "PASS - canonical/map/roster identity ("):
        if not any(line.startswith(prefix) for line in lines):
            raise ValueError(f"Pax complete-gate stage missing from {log}: {prefix}")
    return {
        "tests": int(runs[0][0]), "duration_seconds": runs[0][1], "unittest_outcome": "OK",
        "full_gate_flags": list(flags), "raw_local_log": log.name, "raw_local_log_sha256": sha256(log),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--gate-log", type=Path, required=True)
    parser.add_argument("--baseline-build", type=Path, required=True)
    parser.add_argument("--candidate-build", type=Path, required=True)
    parser.add_argument("--repeat-build", type=Path, required=True)
    args = parser.parse_args()
    source: Path = args.source.resolve()
    review: Path = args.review.resolve()
    evidence: Path = args.evidence.resolve()
    log: Path = args.gate_log.resolve()
    baseline: Path = args.baseline_build.resolve()
    candidate: Path = args.candidate_build.resolve()
    repeated: Path = args.repeat_build.resolve()
    outputs = (baseline, candidate, repeated)
    for path in (review, evidence, log, *outputs, Path(sys.prefix).resolve()):
        require_external(source, path)
    for output in outputs:
        if output.is_relative_to(evidence) or evidence.is_relative_to(output):
            raise ValueError(f"Builds must be outside the bounded artifact directory: {output}")
    if log.is_relative_to(evidence):
        raise ValueError("Raw gate log must be outside the bounded artifact directory")
    for index, output in enumerate(outputs):
        if any(output.is_relative_to(other) or other.is_relative_to(output) for other in outputs[index + 1:]):
            raise ValueError(f"Baseline, candidate and repeated builds must be separate: {outputs}")
    if (evidence / "pax-results.json").exists():
        raise FileExistsError(f"Refusing to overwrite retained Pax results: {evidence}")
    preparation_path = evidence / "preparation.json"
    preparation = require_object(json.loads(preparation_path.read_text(encoding="utf-8")), "Pax preparation")
    review_commit = require_string(preparation["review_commit"], "preparation.review_commit")
    if require_review(review) != review_commit or preparation["executed_review_sha"] != review_commit:
        raise ValueError("Review commit changed after candidate preparation")
    expected_review = read_hashes(preparation["review_files_sha256"], "review_files_sha256")
    observed_review = {relative: tracked_hash(review, review_commit, relative) for relative in REVIEW_FILES}
    if observed_review != expected_review:
        raise ValueError("Review workflow/helper bytes changed after candidate preparation")
    published_patch(review)
    patch_record = require_object(preparation["patch"], "preparation.patch")
    if patch_record["file"] != PATCH_FILE or patch_record["sha256"] != PATCH_SHA256 or preparation["upstream_base"] != BASE:
        raise ValueError("Prepared Pax base/patch differs from the approved published proposal")
    commit = require_string(preparation["temporary_candidate_commit"], "temporary_candidate_commit")
    if git(source, ["rev-parse", "HEAD"]) != commit or git(source, ["show", "-s", "--format=%P", "HEAD"]) != BASE:
        raise ValueError("Pax candidate HEAD or its sole parent differs from recorded preparation")
    if git(source, ["remote", "get-url", "origin"]).removesuffix(".git") != ORIGIN:
        raise ValueError(f"Pax candidate origin changed after preparation; expected {ORIGIN}")
    changes = git(source, ["diff", "--name-status", BASE, "HEAD"]).splitlines()
    if changes != [f"M\t{relative}" for relative in CHANGED_FILES]:
        raise ValueError(f"Candidate committed changes escaped the approved Pax files: {changes}")
    changed_hashes = {relative: sha256(source / relative) for relative in CHANGED_FILES}
    if changed_hashes != read_hashes(preparation["changed_files_sha256"], "changed_files_sha256"):
        raise ValueError("Candidate validator/test bytes changed after preparation")
    require_clean_source(source)
    git(source, ["diff", "--check", BASE, "HEAD"])
    canonical = data_hashes(source)
    if canonical != read_hashes(preparation["canonical_data_sha256"], "canonical_data_sha256"):
        raise ValueError("Complete repository gate changed canonical Pax data")
    gate = collect_gate(log, (source / "VERSION").read_text(encoding="utf-8").strip())
    published = require_object(json.loads((review / "evidence/pax-eligibility-validation.json").read_text(encoding="utf-8")), "Pax evidence")
    results = require_object(published["results"], "Pax evidence.results")
    expected_count = results["candidate_actual_data_full_tests"]
    if type(expected_count) is not int or gate["tests"] != expected_count:
        raise ValueError(f"Executed Pax tests {gate['tests']} differ from published candidate count {expected_count!r}")
    baseline_hashes = public_build_hashes(baseline)
    baseline_record = require_object(preparation["baseline_build"], "preparation.baseline_build")
    if baseline_hashes != read_hashes(baseline_record["files_sha256"], "baseline_build.files_sha256"):
        raise ValueError("Original-source public build changed after preparation")
    candidate_record = generate_build(source, candidate)
    repeated_record = generate_build(source, repeated)
    if baseline_hashes != candidate_record["files_sha256"] or baseline_hashes != repeated_record["files_sha256"]:
        raise ValueError("Original-source, candidate and repeated-candidate public build bytes differ")
    if data_hashes(source) != canonical:
        raise ValueError("Post-gate candidate generation changed canonical Pax data")
    require_clean_source(source)
    git(source, ["diff", "--check", BASE, "HEAD"])
    summary = {
        "scope": "Complete Pax candidate gate and deterministic public builds; browser/CodeQL/release/deployment outcomes are separate",
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "preparation_sha256": sha256(preparation_path), "review_commit": preparation["review_commit"],
        "review_workflow_sha256": preparation["review_workflow_sha256"], "upstream_base": BASE,
        "patch_sha256": PATCH_SHA256, "temporary_candidate_commit": commit,
        "full_gate": gate, "canonical_data_sha256": canonical,
        "canonical_data_files_unchanged": len(canonical), "changed_files_sha256": changed_hashes,
        "baseline_build_sha256": baseline_hashes, "candidate_build": candidate_record,
        "repeated_candidate_build": repeated_record, "all_three_public_builds_byte_identical": True,
        "public_build_files_verified": len(baseline_hashes), "manifest_entries_verified_per_build": len(PUBLIC_FILES),
        "source_clean_including_ignored_outputs": True, "whitespace_check": "PASS",
    }
    (evidence / "pax-results.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
