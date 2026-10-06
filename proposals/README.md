# Candidate changes for maintainer review

These are independent proposals against exact public-source commits, committed only to this review repository. None is applied to Bridge Node 7's repositories, released, or deployed. [TODO.md](../TODO.md) owns the complete implementation scope and acceptance criteria; this file records candidate provenance and actual verification.

| Candidate | Repository/base | Included change | Verification and remaining work |
| --- | --- | --- | --- |
| [M2M source validation](m2m-source-validation.patch) | `materials-to-mission` · `2a8d26af86e8adb8b1e34550045782d1a20418a4` · MIT | Reuse existing public source validator; record actual profile/toolkit version; two useful CLI tests and required generated manifest hashes. | [Verified](../evidence/m2m-source-validation.json): 302-test gate passes locally on Python 3.11–3.13 and in all four hosted Ubuntu/Windows 3.11/3.13 cells; Ubuntu 3.12 consumer path and original targeted 4/4 pass; five checked-in invalid cases plus sentinel rejected before output; deterministic valid receipt and unchanged FMA compatibility preserved. |
| [M2M default-profile documentation](m2m-default-profile-doc.patch) | `materials-to-mission` · same exact base · MIT | T01 companion: correct the linked validation guide's default from `m0-strict-0.2.0` to `m0-strict-0.4.0`; update its manifest entry. | [Standalone navigation verification](../evidence/verification.json): local 300-test gate passes. [Combined local verification](../evidence/m2m-source-validation.json): runtime plus documentation passes 302 tests, 183 manifest entries, deterministic packaging and non-mutating tracked diff on macOS arm64/Python 3.11.16. Combined hosted verification remains unexecuted; upstream acceptance remains open. |
| [FDE timestamp validation](fde-rfc3339-timestamp-contract.patch) | `frontier-decision-engine` · `4a913756d00cdd321da04bf7350507e571f2f2dd` · Apache-2.0 | Validate all four freshness fields against supported RFC3339 syntax/calendar/null rules; three actual-digest tests, generated facts/manifest. | [Verified](../evidence/fde-timestamp-contract.json): targeted 19/19 and Node 229/229 pass on Node 22.23.3 and 24.19.0; timestamp-only full gate failed at context transport on macOS. **Combined complete gate passes locally and on hosted Ubuntu Node 22**, including Python/JavaScript CodeQL with zero reported results. Hosted timestamp-only targeted/Node checks pass; its full browser outcome was not tested. Leap-second policy and millisecond precision remain owner decisions. |
| [FDE context test server](fde-context-threaded-harness.patch) | `frontier-decision-engine` · same exact base · Apache-2.0 | Use native `ThreadingHTTPServer` for the local context harness; remove unused import. | Controlled socket/browser probes reproduce the single-thread blockage; this patch alone passes the original context suite locally and on hosted Ubuntu Node 22. No product UI change or new fallback. |
| [ACA closure links](aca-closure-links.patch) | `ai-cyber-assurance` · `9033bf73bbd3923c5de0a9c6fb9959b4c140de64` · MIT | Require retest links, action/finding consistency and closure membership; three real CLI integration tests and required manifest hashes. | [Verified](../evidence/aca-closure-links.json): 67 tests, 17 repository checks and 73 hashes pass locally and on hosted Ubuntu/Windows Python 3.12; required Ubuntu Python CodeQL completes with zero reported results; 20 invalid variants reject before rendering; original cases and correctly linked additional action pass. |
| [FIW canonical root](fiw-canonical-root.patch) | `frontier-intelligence-workflows` · `36366e96c12765e14d09965c1f82330194dfa8d3` · MIT | One code line canonicalizes the root; two required generated manifests are included. | [Reverified](../evidence/fiw-root-verification.json): 181 tests, compile, ordinary/alias 20/20, 133 hashes and deterministic packaging pass; original source has 32 test errors. |
| [Pax eligibility validation](pax-eligibility-validation.patch) | `pax-silica` · `2f62f678d06f8444ddc7788ce03e1f1f46cf4cba` · MIT | Typed present eligibility dates/source arrays; three added real CLI tests and an unchanged-data positive control. No eligibility cutoff; generic date rules, actual data and locator preserved. | [Verified](../evidence/pax-eligibility-validation.json): 62-test actual-data gate, six focused tests and 44 probes pass (36 invalid rejected, eight valid/optional accepted). Six generated files match baseline/repeated output locally and across all four hosted Ubuntu/Windows Python 3.11/3.12 cells (62 tests each). Both configured CodeQL languages complete with zero reported results. Upstream review/acceptance remains. |
| [Quantum example traceability](quantum-example-traceability.patch) | `quantum-readiness-space-communications` · `0f926377de268b20c2b1223eaf830405b8eb3648` · MIT | Three existing fictional example docs plus manifests: canonical domains, explicit overlapping trace registers, consistent `NOT_ESTABLISHED` coverage. | [Verified](../evidence/quantum-example-traceability.json): 50 tests, 93 hashes, links and deterministic packaging pass; original ledger/posture retained. Approved counting units, support floors and evidence review remain owner decisions. |

## Current source applicability

The October 6 read-only [freshness check](../evidence/verification.json), key `adoption_handoff`, distinguishes textual applicability from runtime acceptance. Original patch files and their tested bases above are unchanged.

| Task | Observed upstream head | Effect on the proposal and next acceptance check |
| --- | --- | --- |
| T01 | `cc10b326dd6185d160ea76939f4089c3f7e1ca91` | One Pages build/workflow/test commit after the recorded base. Both patches pass a combined application check; exporter, validator, profiles and affected tests are unchanged. Rerun the current privacy/full gates after application; earlier 302-test results remain bound to the old base. |
| T02 | `7213151ec3915e513854a8e9d555020b6faff594` | One Pages-portability commit after the recorded base; every patch target file is unchanged and both patches pass a combined application check. Current CI adds a portability stage after `npm run check`; require that stage and configured CodeQL on the accepted candidate. |
| T03 | `9033bf73bbd3923c5de0a9c6fb9959b4c140de64` | Matches the recorded base; application check passes. Maintainer review and the existing upstream checks remain pending. |

No candidate runtime gates were rerun for this handoff. The two new commits do not modify the reviewed validation paths or resolve the FDE contract-policy question. A clean application check does not establish compatibility of the whole newer candidate. Recheck the source head at adoption and review further drift before applying.

## Review and verification

In an authorized candidate checkout, first verify the recorded base and use `git apply --check /path/to/candidate.patch`. That check validates applicability; it does not modify files. Review the diff before applying a candidate. All eight applicability checks passed against the clean audit snapshots; the executed candidate gates and patch hashes are recorded in [verification evidence](../evidence/verification.json). Both FDE patches also apply together, as do the M2M runtime and documentation companions; earlier proposals remain recoverable in review Git history and the local audit cache.

The manually dispatched [hosted candidate workflow](../.github/workflows/candidate-verification.yml) checks T01–T03 in this review repository. It verifies the published source bases and patch hashes, creates disposable candidate commits for clean-tree gates, and runs the declared Ubuntu/Windows checks. FDE and ACA include their required CodeQL analyses, scoped to candidate source with result/database uploads and automatic overlay/TRAP/dependency caching disabled; bounded summaries are retained as workflow artifacts. Source checkouts and temporary commits are never pushed. These runs establish independent candidate results, not upstream adoption or release acceptance. To run the current review branch: `gh workflow run candidate-verification.yml --repo hideouts-io/bridgenode7-technical-review --ref codex/technical-review`. Consult the [verification record](../evidence/verification.json) for completed results, earlier setup failures and the disposition of caches created before the cache controls were corrected. Zero reported CodeQL results applies only to the configured queries and is not an exhaustive security assessment.

### Apply the priority proposals

Run these POSIX-shell commands in separate disposable checkouts at the exact bases in the table, with installed project-supported runtimes. Set `BN7_REVIEW_DIR` to this review checkout and `BN7_VALIDATION_DIR` to an external validation directory. Create the latter before creating environments or writing reports. Verify `git rev-parse HEAD` against the relevant base and inspect `git status --short` before applying anything. Windows maintainers should use their existing workflow's path and environment activation syntax. Preserve the original audit snapshots. Stop on any failed command; each block enables shell failure handling.

Before application, compare each patch's SHA-256 with its existing evidence record: T01 uses `combined_documentation_verification.patch_application_order` in [M2M evidence](../evidence/m2m-source-validation.json), T02 uses `patches` in [FDE evidence](../evidence/fde-timestamp-contract.json), and T03 uses `patch.sha256` in [ACA evidence](../evidence/aca-closure-links.json). The commands reproduce the recorded-base procedures. For adoption at the newer heads above, also inspect and satisfy that head's current workflow, including the additional FDE check below; record its results separately.

The M2M documentation companion is independently applicable at the same base. Its one-sentence correction leaves the historical profile identifiers intact. The commands below apply the runtime proposal first, then the documentation companion. This exact combination passed the local 302-test gate without a generated-evidence refresh; all 184 tracked-file hashes remained unchanged after validation. Existing tests cover rejection before output, deterministic projection/provenance and explicit `m0-strict-0.2.0` compatibility. If adaptation makes evidence stale, use the refresh procedure below, inspect the changes, and repeat the non-mutating gate. The original hosted T01 run did not include this later documentation companion.

M2M uses Python 3.11 or 3.13 in its maintainer matrix; its consumer job uses 3.12. The separate privacy check is part of the workflow, outside the complete repository gate.

```sh
set -eu
python3.11 -m venv "$BN7_VALIDATION_DIR/m2m-venv"
. "$BN7_VALIDATION_DIR/m2m-venv/bin/activate"
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps --no-build-isolation -e .
git apply --check "$BN7_REVIEW_DIR/proposals/m2m-source-validation.patch"
git apply "$BN7_REVIEW_DIR/proposals/m2m-source-validation.patch"
git apply --check "$BN7_REVIEW_DIR/proposals/m2m-default-profile-doc.patch"
git apply "$BN7_REVIEW_DIR/proposals/m2m-default-profile-doc.patch"
export PYTHONPATH="$PWD/src"
python -c 'from pathlib import Path; import materials_to_mission as m; p = Path(m.__file__).resolve(); assert p.is_relative_to(Path.cwd().resolve() / "src"), p; print(p)'
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

For the newer FDE head above, [current CI](https://github.com/Bridge-Node-7/frontier-decision-engine/blob/7213151ec3915e513854a8e9d555020b6faff594/.github/workflows/ci.yml) additionally checks the deployment artifact after `npm run check`. In that adopted candidate checkout, use fresh output directories under the existing validation directory:

```sh
set -eu
python scripts/build_pages.py --source site --output "$BN7_VALIDATION_DIR/fde-pages-current"
diff -qr site "$BN7_VALIDATION_DIR/fde-pages-current"
python scripts/build_pages.py --source site --output "$BN7_VALIDATION_DIR/fde-pages-portable" --public-url "https://portable.example/frontier-decision-engine/"
```

These are local artifact checks, not a Pages deployment. The earlier reviewed base does not contain `scripts/build_pages.py`, so this block applies only after selecting the newer source. Required CodeQL and other current upstream checks remain part of maintainer acceptance.

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

### Acceptance and recovery

Record maintainer acceptance, the implemented upstream commit, and that commit's required check links under the existing [TODO task](../TODO.md#ownership-and-publication-state). Passing the independent candidate checks alone does not close it. T02 also needs the owner's timestamp-policy record. Release and deployment decisions remain separate.

- **M2M:** the source changes can be reverted without a schema migration, but that restores the known source-validation gap. Stop relying on affected projections until an accepted implementation is in place. Require exporter success and match the intended source and artifact digests before consuming output; failed runs can leave older files. Identify and regenerate or withdraw affected distributed projections as appropriate.
- **ACA:** reverting the validator restores the inconsistent-closure acceptance gap. Revalidate the underlying cases and regenerate affected communication artifacts from an accepted implementation; no candidate test establishes that a real corrective action is complete.
- **FDE:** review rollback of timestamp validation and the test-server change independently. Restoring the old timestamp path restores the malformed-date gap; changing policy does not itself require undoing the harness fix. Preserve original packets, refresh facts/manifests through the existing commands after adaptation, and repeat the accepted configuration's gates.

Pax's revised proposal accepts the owner-intended record from [PR #50](https://github.com/Bridge-Node-7/pax-silica/pull/50), preserving its dates and all generic `verified_at` limits. Its [current evidence](../evidence/pax-eligibility-validation.json) records actual-data verification and immutable references to the previous patch and synthetic results. New pairing/minimum-source or chronology rules require an explicit owner contract. Run the following in a disposable Pax checkout at the table's exact base, with the same external `BN7_REVIEW_DIR` and `BN7_VALIDATION_DIR` variables described above:

```sh
set -eu
python3.12 -m venv "$BN7_VALIDATION_DIR/pax-venv"
. "$BN7_VALIDATION_DIR/pax-venv/bin/activate"
git apply --check "$BN7_REVIEW_DIR/proposals/pax-eligibility-validation.patch"
git apply "$BN7_REVIEW_DIR/proposals/pax-eligibility-validation.patch"
git --no-pager diff --binary HEAD > "$BN7_VALIDATION_DIR/pax-before-validation.patch"
python -m unittest discover -s tests -p 'test_snapshot_boundary.py' -v
python scripts/check_repo.py
git --no-pager diff --binary HEAD > "$BN7_VALIDATION_DIR/pax-after-validation.patch"
cmp "$BN7_VALIDATION_DIR/pax-before-validation.patch" "$BN7_VALIDATION_DIR/pax-after-validation.patch"
git --no-pager diff --check
```

The Pax full gate includes actual-data validation, deterministic generation, evidence integrity, public-boundary/readability checks and all tests. No generated files need refresh for this patch. The separate [Pax hosted workflow](../.github/workflows/pax-candidate-verification.yml) has passed all four Ubuntu/Windows Python 3.11/3.12 cells, both configured CodeQL language analyses and the aggregate status check. It verifies the exact base/patch, creates an unpushed temporary candidate commit, checks unchanged data and baseline/repeated builds, and retains bounded evidence. CodeQL verifies candidate database roots and changed Python or unchanged JavaScript source bytes; result/database uploads and automatic persistent analysis caches are disabled. The [verification record](../evidence/pax-eligibility-validation.json) pins the executed workflow and helper hashes. A fresh review-only run can be dispatched with `gh workflow run pax-candidate-verification.yml --repo hideouts-io/bridgenode7-technical-review --ref codex/technical-review`. After adaptation, maintainers still run applicable upstream acceptance checks; independent hosted results do not establish branch-protection parity or authorize adoption. Browser checks are needed if subsequent changes affect public output; this revision's six generated files are byte-identical to baseline on every checked platform.

Quantum includes only required example/manifest changes. After adaptation, run `python tools/generate_manifest.py`, review the generated diff, and run `bash scripts/validate.sh`; do not replace `NOT_ESTABLISHED` with a percentage until the recorded owner decisions and evidence review are complete.

The repository licenses remain applicable to their fragments; source provenance is explicit above. Share each patch with its linked verification record, which retains the upstream MIT or Apache 2.0 license. FMA's proprietary policy is respected by providing the [evaluation-only specification](../evidence/fma-criticality-specification.json), with fourteen unchanged-source CLI results and no proprietary source patch.
