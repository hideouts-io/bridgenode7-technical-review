# Candidate changes for maintainer review

These are independent proposals against exact public-source commits, committed only to this review repository. None is applied to Bridge Node 7's repositories, released, or deployed. [TODO.md](../TODO.md) owns the complete implementation scope and acceptance criteria; this file records candidate provenance and actual verification.

| Candidate | Repository/base | Included change | Verification and remaining work |
| --- | --- | --- | --- |
| [M2M source validation](m2m-source-validation.patch) | `materials-to-mission` · `2a8d26af86e8adb8b1e34550045782d1a20418a4` · MIT | Reuse existing public source validator; record actual profile/toolkit version; two useful CLI tests and required generated manifest hashes. | [Verified](../evidence/m2m-source-validation.json): 302-test gate passes locally on Python 3.11–3.13 and in all four hosted Ubuntu/Windows 3.11/3.13 cells; Ubuntu 3.12 consumer path and original targeted 4/4 pass; five checked-in invalid cases plus sentinel rejected before output; deterministic valid receipt and unchanged FMA compatibility preserved. |
| [FDE timestamp validation](fde-rfc3339-timestamp-contract.patch) | `frontier-decision-engine` · `4a913756d00cdd321da04bf7350507e571f2f2dd` · Apache-2.0 | Validate all four freshness fields against supported RFC3339 syntax/calendar/null rules; three actual-digest tests, generated facts/manifest. | [Verified](../evidence/fde-timestamp-contract.json): targeted 19/19 and Node 229/229 pass on Node 22.23.3 and 24.19.0; timestamp-only full gate failed at context transport on macOS. **Combined complete gate passes locally and on hosted Ubuntu Node 22**, including Python/JavaScript CodeQL with zero reported results. Hosted timestamp-only targeted/Node checks pass; its full browser outcome was not tested. Leap-second policy and millisecond precision remain owner decisions. |
| [FDE context test server](fde-context-threaded-harness.patch) | `frontier-decision-engine` · same exact base · Apache-2.0 | Use native `ThreadingHTTPServer` for the local context harness; remove unused import. | Controlled socket/browser probes reproduce the single-thread blockage; this patch alone passes the original context suite locally and on hosted Ubuntu Node 22. No product UI change or new fallback. |
| [ACA closure links](aca-closure-links.patch) | `ai-cyber-assurance` · `9033bf73bbd3923c5de0a9c6fb9959b4c140de64` · MIT | Require retest links, action/finding consistency and closure membership; three real CLI integration tests and required manifest hashes. | [Verified](../evidence/aca-closure-links.json): 67 tests, 17 repository checks and 73 hashes pass locally and on hosted Ubuntu/Windows Python 3.12; required Ubuntu Python CodeQL completes with zero reported results; 20 invalid variants reject before rendering; original cases and correctly linked additional action pass. |
| [FIW canonical root](fiw-canonical-root.patch) | `frontier-intelligence-workflows` · `36366e96c12765e14d09965c1f82330194dfa8d3` · MIT | One code line canonicalizes the root; two required generated manifests are included. | [Reverified](../evidence/fiw-root-verification.json): 181 tests, compile, ordinary/alias 20/20, 133 hashes and deterministic packaging pass; original source has 32 test errors. |
| [Pax eligibility validation](pax-eligibility-validation.patch) | `pax-silica` · `2f62f678d06f8444ddc7788ce03e1f1f46cf4cba` · MIT | Typed present eligibility dates/source arrays; three real CLI tests. Actual data, locator and distribution remain unchanged. | [Verified](../evidence/pax-eligibility-validation.json): 38 probes reject, including the disputed cutoff case; seven controls pass. Prior 62-test gate passed only with a synthetic date. **Full patch requires chronology-policy revision before adoption:** its cutoff guard rejects the separate field-review date intentionally recorded in owner PR #50. |
| [Quantum example traceability](quantum-example-traceability.patch) | `quantum-readiness-space-communications` · `0f926377de268b20c2b1223eaf830405b8eb3648` · MIT | Three existing fictional example docs plus manifests: canonical domains, explicit overlapping trace registers, consistent `NOT_ESTABLISHED` coverage. | [Verified](../evidence/quantum-example-traceability.json): 50 tests, 93 hashes, links and deterministic packaging pass; original ledger/posture retained. Approved counting units, support floors and evidence review remain owner decisions. |

## Review and verification

In an authorized candidate checkout, first verify the recorded base and use `git apply --check /path/to/candidate.patch`. That check validates applicability; it does not modify files. Review the diff before applying a candidate. All seven applicability checks passed against the clean audit snapshots; the executed candidate gates and patch hashes are recorded in [verification evidence](../evidence/verification.json). Both FDE patches also apply together; earlier proposals remain recoverable in review Git history and the local audit cache.

The manually dispatched [hosted candidate workflow](../.github/workflows/candidate-verification.yml) checks T01–T03 in this review repository. It verifies the published source bases and patch hashes, creates disposable candidate commits for clean-tree gates, and runs the declared Ubuntu/Windows checks. FDE and ACA include their required CodeQL analyses, scoped to candidate source with result/database uploads and automatic overlay/TRAP/dependency caching disabled; bounded summaries are retained as workflow artifacts. Source checkouts and temporary commits are never pushed. These runs establish independent candidate results, not upstream adoption or release acceptance. To run the current review branch: `gh workflow run candidate-verification.yml --repo hideouts-io/bridgenode7-technical-review --ref codex/technical-review`. Consult the [verification record](../evidence/verification.json) for completed results, earlier setup failures and the disposition of caches created before the cache controls were corrected. Zero reported CodeQL results applies only to the configured queries and is not an exhaustive security assessment.

### Apply the priority proposals

Run these POSIX-shell commands in separate disposable checkouts at the exact bases in the table, with installed project-supported runtimes. Set `BN7_REVIEW_DIR` to this review checkout and `BN7_VALIDATION_DIR` to an external validation directory. Create the latter before creating environments or writing reports. Verify `git rev-parse HEAD` against the relevant base and inspect `git status --short` before applying anything. Windows maintainers should use their existing workflow's path and environment activation syntax. Preserve the original audit snapshots. Stop on any failed command; each block enables shell failure handling.

M2M uses Python 3.11 or 3.13 in its maintainer matrix; its consumer job uses 3.12. The separate privacy check is part of the workflow, outside the complete repository gate.

```sh
set -eu
python3.11 -m venv "$BN7_VALIDATION_DIR/m2m-venv"
. "$BN7_VALIDATION_DIR/m2m-venv/bin/activate"
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps --no-build-isolation -e .
git apply --check "$BN7_REVIEW_DIR/proposals/m2m-source-validation.patch"
git apply "$BN7_REVIEW_DIR/proposals/m2m-source-validation.patch"
git --no-pager diff --binary HEAD > "$BN7_VALIDATION_DIR/m2m-before-validation.patch"
python scripts/check_privacy.py
python scripts/check_repo.py
git --no-pager diff --binary HEAD > "$BN7_VALIDATION_DIR/m2m-after-validation.patch"
cmp "$BN7_VALIDATION_DIR/m2m-before-validation.patch" "$BN7_VALIDATION_DIR/m2m-after-validation.patch"
git --no-pager diff --check
```

FDE's workflow uses Node 22. Put that runtime on `PATH` before the commands below. Its declared browser dependency is in `requirements-dev.txt`; install its matching Chromium in the selected environment. The plain browser installation below assumes OS prerequisites are present; Ubuntu workflow parity requires its existing `python -m playwright install --with-deps chromium` step. Review the timestamp and harness diffs separately before applying both for the complete-gate configuration. In separate fresh copies, timestamp-only acceptance uses `node --test tests/governed-context.test.js` and `npm test`; harness-only acceptance uses `npm run test:context` on unchanged product source. Preserve the timestamp-only full-gate failure separately from the combined pass.

```sh
set -eu
python3.11 -m venv "$BN7_VALIDATION_DIR/fde-venv"
. "$BN7_VALIDATION_DIR/fde-venv/bin/activate"
python -m pip install --disable-pip-version-check -r requirements-dev.txt
python -m playwright install chromium
node --version
npm --version
npm ci --ignore-scripts --no-audit --no-fund
git apply --check "$BN7_REVIEW_DIR/proposals/fde-rfc3339-timestamp-contract.patch" "$BN7_REVIEW_DIR/proposals/fde-context-threaded-harness.patch"
git apply "$BN7_REVIEW_DIR/proposals/fde-rfc3339-timestamp-contract.patch"
git apply "$BN7_REVIEW_DIR/proposals/fde-context-threaded-harness.patch"
git --no-pager diff --binary HEAD > "$BN7_VALIDATION_DIR/fde-before-validation.patch"
npm run manifest
npm run facts
npm run manifest
npm run check
git --no-pager diff --binary HEAD > "$BN7_VALIDATION_DIR/fde-after-validation.patch"
cmp "$BN7_VALIDATION_DIR/fde-before-validation.patch" "$BN7_VALIDATION_DIR/fde-after-validation.patch"
git --no-pager diff --check
```

ACA's validation workflow uses Python 3.12 and the standard library; its hash step requires `sha256sum` on `PATH`.

```sh
set -eu
python3.12 -m venv "$BN7_VALIDATION_DIR/aca-venv"
. "$BN7_VALIDATION_DIR/aca-venv/bin/activate"
git apply --check "$BN7_REVIEW_DIR/proposals/aca-closure-links.patch"
git apply "$BN7_REVIEW_DIR/proposals/aca-closure-links.patch"
git --no-pager diff --binary HEAD > "$BN7_VALIDATION_DIR/aca-before-validation.patch"
python -m unittest discover -s tests -p 'test_*.py'
python scripts/refresh_release_metadata.py --root . --check
python scripts/validate_repo.py --root . --json-output "$BN7_VALIDATION_DIR/aca-validation.json"
sha256sum -c MANIFEST.sha256
git --no-pager diff --binary HEAD > "$BN7_VALIDATION_DIR/aca-after-validation.patch"
cmp "$BN7_VALIDATION_DIR/aca-before-validation.patch" "$BN7_VALIDATION_DIR/aca-after-validation.patch"
git --no-pager diff --check
```

The exact M2M/ACA/FIW patches include required manifest hashes, and FDE includes facts/manifest. After adaptation, regenerate through established commands and inspect the generated diff before capturing the reviewed candidate state and repeating the corresponding non-mutating gate: M2M `python scripts/check_repo.py --update-evidence`; ACA `python scripts/refresh_release_metadata.py --root . --write`, then `--check`; FDE's refresh sequence is shown above. An uncommitted applied patch is an expected tracked diff. The before/after `cmp` checks gate-induced tracked-byte drift; `git diff --check` checks whitespace. Hosted `git diff --exit-code` assumes the candidate is committed. No commit to an upstream repository is part of this external review.

Pax's preserved proposal rejects the owner-intended record from [PR #50](https://github.com/Bridge-Node-7/pax-silica/pull/50); it is not ready to adopt as written. Its type/reference checks remain useful, but the global snapshot-cutoff extension requires revision. Preserve the declared dates and historical synthetic-test results. Any new pairing/minimum-source or chronology requirement needs an explicit field contract. Require the revised candidate's existing full gate on unchanged actual data before adoption; no such revised gate is asserted here.

Quantum includes only required example/manifest changes. After adaptation, run `python tools/generate_manifest.py`, review the generated diff, and run `bash scripts/validate.sh`; do not replace `NOT_ESTABLISHED` with a percentage until the recorded owner decisions and evidence review are complete.

The repository licenses remain applicable to their fragments; source provenance is explicit above. Share each patch with its linked verification record, which retains the upstream MIT or Apache 2.0 license. FMA's proprietary policy is respected by providing the [evaluation-only specification](../evidence/fma-criticality-specification.json), with fourteen unchanged-source CLI results and no proprietary source patch.
