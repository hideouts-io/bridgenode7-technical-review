"""Verify Pax CodeQL attribution and retain counts without source snippets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import TypedDict, cast
from zipfile import ZipFile

from collect_codeql import collect_run
from prepare_candidate import require_list, require_object, require_string


class Finding(TypedDict):
    rule_id: str
    files: list[str]


class RunSummary(TypedDict):
    tool: str
    tool_version: str
    result_count: int
    findings: list[Finding]


class DatabaseVerification(TypedDict):
    source_root_verified: bool
    source_language_verified: str
    archived_source_bytes_verified: dict[str, str]


class AnalysisSummary(TypedDict):
    language: str
    source_change_scope: str
    source_byte_coverage: str
    sarif_sha256: str
    database: DatabaseVerification
    runs: list[RunSummary]


class Summary(TypedDict):
    scope: str
    analyses: list[AnalysisSummary]


def verify_database(
    codeql: Path,
    database: Path,
    source: Path,
    language: str,
    relative_files: tuple[str, ...],
) -> DatabaseVerification:
    """Bind a language database to the candidate and its selected source bytes."""
    command: list[str] = [str(codeql), "resolve", "database", str(database), "--format=json"]
    try:
        result = subprocess.run(
            command, check=True, text=True, encoding="utf-8", capture_output=True,
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"CodeQL database resolution failed: command={error.cmd}; "
            f"exit={error.returncode}; stdout={error.stdout}; stderr={error.stderr}"
        ) from error
    raw_metadata: object = json.loads(result.stdout)
    metadata = require_object(raw_metadata, "CodeQL database metadata")
    prefix = Path(require_string(metadata["sourceLocationPrefix"], "database sourceLocationPrefix"))
    if prefix.resolve() != source:
        raise ValueError(f"CodeQL database root {prefix} does not identify Pax candidate {source}")
    languages: list[str] = [
        require_string(value, "database language")
        for value in require_list(metadata["languages"], "database languages")
    ]
    if languages != [language]:
        raise ValueError(f"Expected single database language {language}; found {languages} in {database}")
    archive_path = Path(require_string(metadata["sourceArchiveZip"], "database sourceArchiveZip"))
    archive_prefix: str = source.as_posix().lstrip("/") + "/"
    verified: dict[str, str] = {}
    with ZipFile(archive_path) as archive:
        names: dict[str, str] = {name.lstrip("/"): name for name in archive.namelist()}
        for relative in relative_files:
            member: str = archive_prefix + relative
            if member not in names:
                raise ValueError(f"Pax source file missing from CodeQL archive {archive_path}: {relative}")
            archived: str = hashlib.sha256(archive.read(names[member])).hexdigest()
            current: str = hashlib.sha256((source / relative).read_bytes()).hexdigest()
            if archived != current:
                raise ValueError(
                    f"CodeQL archived different Pax source bytes for {relative}: "
                    f"archived={archived}; candidate={current}"
                )
            verified[relative] = archived
    return {
        "source_root_verified": True,
        "source_language_verified": language,
        "archived_source_bytes_verified": verified,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--sarif", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--codeql", type=Path, required=True)
    parser.add_argument("--databases", type=Path, required=True)
    parser.add_argument("--language", choices=("python", "javascript"), required=True)
    args = parser.parse_args()
    source: Path = args.source.resolve()
    sarif: Path = args.sarif.resolve()
    evidence: Path = args.evidence.resolve()
    codeql: Path = args.codeql.resolve()
    databases: Path = args.databases.resolve()
    language: str = args.language
    relative_files: tuple[str, ...]
    source_change_scope: str
    if language == "python":
        relative_files = ("scripts/validate_data.py", "tests/test_snapshot_boundary.py")
        source_change_scope = "Changed Pax validator and CLI regression tests"
    else:
        relative_files = ("web/app.js",)
        source_change_scope = "Unchanged published Pax JavaScript application; no JavaScript patch is claimed"
    observed: list[str] = sorted(path.stem for path in sarif.glob("*.sarif"))
    if observed != [language]:
        raise ValueError(f"Expected only {language}.sarif in {sarif}; found {observed}")
    path: Path = sarif / f"{language}.sarif"
    raw_document: object = json.loads(path.read_text(encoding="utf-8"))
    document = require_object(raw_document, "SARIF document")
    runs: list[object] = require_list(document["runs"], "SARIF runs")
    if not runs:
        raise ValueError(f"No CodeQL analysis runs in {path}")
    analysis: AnalysisSummary = {
        "language": language,
        "source_change_scope": source_change_scope,
        "source_byte_coverage": (
            "Selected candidate files verified in the database archive; "
            "this does not establish exhaustive file or query coverage"
        ),
        "sarif_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "database": verify_database(codeql, databases / language, source, language, relative_files),
        "runs": [cast(RunSummary, collect_run(run, source)) for run in runs],
    }
    output: Summary = {
        "scope": "Pax candidate analysis only; execution success does not imply zero findings",
        "analyses": [analysis],
    }
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "codeql-summary.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
