"""Check SARIF source attribution and retain bounded analysis metadata, without snippets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote, urlparse

from prepare_candidate import require_list, require_object, require_string


def collect_run(value: object, source: Path) -> dict[str, object]:
    run = require_object(value, "SARIF run")
    tool = require_object(run["tool"], "SARIF tool")
    driver = require_object(tool["driver"], "SARIF driver")
    name = require_string(driver["name"], "SARIF driver.name")
    if name != "CodeQL":
        raise ValueError(f"Expected CodeQL SARIF, found {name}")
    bases = require_object(run["originalUriBaseIds"], "SARIF originalUriBaseIds")
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
            if artifact.get("uriBaseId") != "%SRCROOT%":
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
        "tool": name, "tool_version": driver.get("semanticVersion", driver.get("version")),
        "source_root_verified": True, "result_count": len(results), "findings": findings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--sarif", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
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
            "runs": [collect_run(run, source) for run in runs],
        })
    args.evidence.mkdir(parents=True, exist_ok=True)
    output = {"scope": "candidate analysis only; execution success does not imply zero findings", "analyses": summaries}
    (args.evidence / "codeql-summary.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
