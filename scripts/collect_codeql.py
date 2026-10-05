"""Check SARIF source attribution and retain bounded analysis metadata, without snippets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlparse
from zipfile import ZipFile

from prepare_candidate import require_list, require_object, require_string


def verify_database(codeql: Path, database: Path, source: Path, language: str, evidence: Path) -> dict[str, object]:
    """Verify the database root and archived bytes of candidate implementation changes."""
    result = subprocess.run(
        [str(codeql), "resolve", "database", str(database), "--format=json"],
        check=True, text=True, encoding="utf-8", stdout=subprocess.PIPE,
    )
    metadata = require_object(json.loads(result.stdout), "CodeQL database metadata")
    prefix = Path(require_string(metadata["sourceLocationPrefix"], "database sourceLocationPrefix"))
    if prefix.resolve() != source:
        raise ValueError(f"CodeQL database root {prefix} does not identify {source}")
    languages = [require_string(value, "database language")
                 for value in require_list(metadata["languages"], "database languages")]
    if language not in languages:
        raise ValueError(f"Expected database language {language}; found {languages}")
    archive_path = Path(require_string(metadata["sourceArchiveZip"], "database sourceArchiveZip"))
    preparation = require_object(json.loads((evidence / "preparation.json").read_text()), "preparation")
    changes = [require_string(value, "changed file") for value in require_list(preparation["changed_files"], "changed_files")]
    suffixes = {"python": {".py"}, "javascript": {".js", ".mjs", ".cjs", ".ts"}}
    expected = [name for name in changes if Path(name).suffix in suffixes[language]]
    if not expected:
        raise ValueError(f"No changed {language} implementation files to verify in the database")
    archive_prefix = source.as_posix().lstrip("/") + "/"
    verified: dict[str, str] = {}
    with ZipFile(archive_path) as archive:
        names = {name.lstrip("/"): name for name in archive.namelist()}
        for relative in expected:
            member = archive_prefix + relative
            if member not in names:
                raise ValueError(f"Candidate implementation missing from CodeQL source archive: {relative}")
            archived = hashlib.sha256(archive.read(names[member])).hexdigest()
            current = hashlib.sha256((source / relative).read_bytes()).hexdigest()
            if archived != current:
                raise ValueError(f"CodeQL archived different candidate bytes for {relative}: {archived}")
            verified[relative] = archived
    return {"source_root_verified": True, "changed_source_bytes_verified": verified}


def collect_run(value: object, source: Path) -> dict[str, object]:
    run = require_object(value, "SARIF run")
    tool = require_object(run["tool"], "SARIF tool")
    driver = require_object(tool["driver"], "SARIF driver")
    name = require_string(driver["name"], "SARIF driver.name")
    if name != "CodeQL":
        raise ValueError(f"Expected CodeQL SARIF, found {name}")
    if "originalUriBaseIds" in run:
        bases = require_object(run["originalUriBaseIds"], "SARIF originalUriBaseIds")
        if "%SRCROOT%" in bases:
            root = require_object(bases["%SRCROOT%"], "SARIF %SRCROOT%")
            uri = require_string(root["uri"], "SARIF source URI")
            if uri.rstrip("/") != source.as_uri().rstrip("/"):
                raise ValueError(f"SARIF source root {uri} does not identify {source}")
    results = require_list(run["results"], "SARIF results")
    findings: list[dict[str, object]] = []
    for value in results:
        result = require_object(value, "SARIF result")
        locations = require_list(result["locations"], "SARIF result locations")
        paths: list[str] = []
        for location_value in locations:
            location = require_object(location_value, "SARIF location")
            physical = require_object(location["physicalLocation"], "SARIF physicalLocation")
            artifact = require_object(physical["artifactLocation"], "SARIF artifactLocation")
            if "uriBaseId" in artifact and artifact["uriBaseId"] != "%SRCROOT%":
                raise ValueError(f"SARIF result uses an unverified URI base: {artifact.get('uriBaseId')}")
            relative = require_string(artifact["uri"], "SARIF artifact URI")
            if urlparse(relative).scheme:
                raise ValueError(f"Expected a source-relative SARIF location: {relative}")
            path = (source / unquote(relative)).resolve()
            if not path.is_relative_to(source) or not path.is_file():
                raise ValueError(f"SARIF result location is outside the candidate source: {relative}")
            paths.append(path.relative_to(source).as_posix())
        findings.append({"rule_id": require_string(result["ruleId"], "SARIF ruleId"), "files": paths})
    return {
        "tool": name, "tool_version": require_string(
            driver["semanticVersion"] if "semanticVersion" in driver else driver["version"], "SARIF tool version"),
        "result_count": len(results), "findings": findings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--sarif", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--codeql", type=Path, required=True)
    parser.add_argument("--databases", type=Path, required=True)
    parser.add_argument("--language", action="append", required=True)
    args = parser.parse_args()
    source: Path = args.source.resolve()
    expected: list[str] = args.language
    summaries: list[dict[str, object]] = []
    observed = sorted(path.stem for path in args.sarif.glob("*.sarif"))
    if observed != sorted(expected):
        raise ValueError(f"Expected SARIF languages {expected}; found {observed}")
    for language in expected:
        path = args.sarif / f"{language}.sarif"
        document = require_object(json.loads(path.read_text(encoding="utf-8")), "SARIF document")
        runs = require_list(document["runs"], "SARIF runs")
        if not runs:
            raise ValueError(f"No analysis runs in {path}")
        summaries.append({
            "language": language, "sarif_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "database": verify_database(args.codeql, args.databases / language, source, language, args.evidence),
            "runs": [collect_run(run, source) for run in runs],
        })
    args.evidence.mkdir(parents=True, exist_ok=True)
    output = {"scope": "candidate analysis only; execution success does not imply zero findings", "analyses": summaries}
    (args.evidence / "codeql-summary.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
