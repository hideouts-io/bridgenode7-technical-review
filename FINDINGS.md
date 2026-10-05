# Evidence-backed findings

**Independent public-source review · October 4, 2026 · America/Los_Angeles.** Source identities are fixed in [inventory.csv](inventory.csv). Results describe those commits and the local environments used; they do not establish defects in private systems or deployed customer workloads. [Verification evidence](evidence/verification.json) records commands, outcomes, candidate scope, and local log provenance. Implementation actions and acceptance checks live in [TODO.md](TODO.md).

Priority expresses recommended work order: **P1** addresses inconsistent machine acceptance or source-policy enforcement; **P2** addresses controlled validation failures, onboarding, provenance, or instructional consistency. No emergency, exploitability, or operational-severity claim is made.

## F01

**P1 · Materials-to-Mission exports cases that its existing source validator rejects.** Confirmed producer validation gap.

The exporter checks synthetic/public-safe declarations and validates projected artifacts against pinned FMA schemas, but does not invoke M2M's case validator before projection. Its documentation correctly limits PASS to deterministic transformation and contract conformance. That narrower guarantee does not enforce the source repository's existing public-boundary or critical-condition policies.

With the unchanged CLI, a synthetic boundary-marker case rejected by `validate_case` as `PUBLIC_BOUNDARY` exports successfully and carries the marker into the graph. The checked-in `triggered-critical-advance.json` is rejected as `CRITICAL_CONDITION`, yet exports successfully with an `APPROVE` disposition projected from the source's proposed advance. The current FMA consumer accepts the resulting portable graph/receipt structurally. These are synthetic local probes; no real protected information was exported, and the projected disposition grants no decision authority.

Evidence: [exporter's declaration checks](https://github.com/Bridge-Node-7/materials-to-mission/blob/2a8d26af86e8adb8b1e34550045782d1a20418a4/scripts/export_fma_projection.py#L108-L116), [output-contract validation](https://github.com/Bridge-Node-7/materials-to-mission/blob/2a8d26af86e8adb8b1e34550045782d1a20418a4/scripts/export_fma_projection.py#L367-L381), [existing invalid case](https://github.com/Bridge-Node-7/materials-to-mission/blob/2a8d26af86e8adb8b1e34550045782d1a20418a4/examples/invalid/triggered-critical-advance.json), and [declared interoperability/assurance boundary](https://github.com/Bridge-Node-7/materials-to-mission/blob/2a8d26af86e8adb8b1e34550045782d1a20418a4/docs/FMA_INTEROPERABILITY.md#L49-L66).

Reproduce by running the documented exporter against the checked-in invalid case, then compare its successful exit with the public `m0-strict-0.4.0` source-validation result. The smallest correction reuses that existing validator before producing output; it does not ask FMA to infer materials-domain policy. See [T01](TODO.md#t01).

## F02

**P1 · Frontier Decision Engine treats invalid nullable freshness dates as current.** Confirmed runtime/contract discrepancy.

The Decision Context Packet 0.3.0 schema permits a date-time string or explicit null for `review_due_at` and `valid_until`. Runtime parsing returns null for an invalid value and then treats it like an absent deadline. A valid review deadline can therefore make a packet with malformed expiry appear CURRENT and eligible for active preparation.

At a fixed synthetic evaluation time of `2026-09-14T00:00:00Z`, packets with recomputed integrity digests and `valid_until` set to `not-a-date` or the number `42` both return `valid: true`, `activeEligible: true`, and freshness `CURRENT`. The parseable string `September 16, 2026` is also accepted, although explicit JSON Schema format assertion rejects it. Integrity verification does not validate the meaning or type of the hashed fields.

Evidence: [published nullable date-time contract](https://github.com/Bridge-Node-7/frontier-decision-engine/blob/4a913756d00cdd321da04bf7350507e571f2f2dd/site/schemas/mission-graph-decision-context-0.3.0.schema.json#L93-L105), [freshness computation](https://github.com/Bridge-Node-7/frontier-decision-engine/blob/4a913756d00cdd321da04bf7350507e571f2f2dd/site/src/lib/governed-context.js#L145-L160), and [active-eligibility decision](https://github.com/Bridge-Node-7/frontier-decision-engine/blob/4a913756d00cdd321da04bf7350507e571f2f2dd/site/src/lib/governed-context.js#L242-L245).

The current candidate rejects malformed types, syntax and calendar values in all four freshness fields, including the parseable non-contract string. It preserves the runtime-supported non-leap-second RFC3339 subset; the contract owner must explicitly document that subset or decide on a deliberate leap-second policy. Native Date precision remains milliseconds. [JSON Schema's format documentation](https://json-schema.org/understanding-json-schema/reference/string#format) explains why declaring a format alone is not an assertion in every validator. See [T02](TODO.md#t02).

Separate verification work identified a local test-harness defect: preopened connections block the context suite's single-threaded HTTP server. Controlled socket and browser probes reproduce the blockage, and Python's native [ThreadingHTTPServer](https://docs.python.org/3.11/library/http.server.html#http.server.ThreadingHTTPServer) corrects it. Timestamp-only targeted/Node checks pass but its full gate fails at that handoff; the independent harness patch passes the original context suite, and both patches together pass the full 229-test/browser gate. [Evidence](evidence/fde-timestamp-contract.json) preserves the failed run and diagnostics. This is a test-server correction, not proof that timestamp validation fixes network transport.

## F03

**P1 · AI Cyber Assurance accepts a closed finding with a disconnected retest action.** Confirmed required-field and relationship gaps.

Starting with the checked-in synthetic AI-agent case, removing `retests[0].corrective_action_ref` still yields CLI PASS. Changing the reference from `CA-001` to `CA-002`, which belongs to another finding, also yields PASS and allows all three downstream communication views to render. The record retains its closed finding.

The missing-field case violates the published schema's required fields. The cross-wired case is schema-valid but violates the documented relationship among a finding, its corrective action, and its retest. Existing checks validate the retest's finding and the closure actions separately without establishing that they describe the same corrective-action path. This demonstrates inconsistent synthetic records accepted by the machine; it does not establish that a real control deficiency was falsely closed.

Evidence: [documented closure invariants](https://github.com/Bridge-Node-7/ai-cyber-assurance/blob/9033bf73bbd3923c5de0a9c6fb9959b4c140de64/13-assurance-intelligence/README.md#L72-L80), [required retest fields](https://github.com/Bridge-Node-7/ai-cyber-assurance/blob/9033bf73bbd3923c5de0a9c6fb9959b4c140de64/13-assurance-intelligence/schemas/assurance-case.schema.json#L268-L276), [retest validation](https://github.com/Bridge-Node-7/ai-cyber-assurance/blob/9033bf73bbd3923c5de0a9c6fb9959b4c140de64/scripts/validate_assurance_case.py#L367-L381), and [closure checks](https://github.com/Bridge-Node-7/ai-cyber-assurance/blob/9033bf73bbd3923c5de0a9c6fb9959b4c140de64/scripts/validate_assurance_case.py#L410-L426).

Reproduce the two edits in external copies of `10-examples/synthetic-ai-agent-assurance/assurance-case.json`; run `scripts/validate_assurance_case.py <fixture> --as-of 2026-10-04` and the renderer against the cross-wired copy. Require the links and compare their finding/action identities using the existing validator. No new graph framework or dependency is needed. See [T03](TODO.md#t03).

## F04

**P2 · Frontier Intelligence Workflows' documented verification fails on macOS path aliases.** Confirmed reproducibility defect.

Normal macOS temporary directories can be named through `/var` while their resolved files appear through `/private/var`. FIW's scanner resolves file paths, but its wrapper passes an unresolved root to a lexical `relative_to` comparison. The test and compile gates raise `ValueError` before completing their checks.

On unchanged source, 181 tests execute with 32 errors on both Python 3.11.16 and 3.14.7; the compile gate fails for the same cause. Ordinary repository validation still passes 20/20. An independent reproduction uses identical source bytes and a real Git index through a temporary-path alias: the alias fails, while resolving the root succeeds. The local candidate adds one root-resolution line and refreshes the two existing sealed manifests. Existing 181 tests, compile checks, and 20/20 validator controls then pass on Python 3.11.16.

Evidence: [documented commands](https://github.com/Bridge-Node-7/frontier-intelligence-workflows/blob/36366e96c12765e14d09965c1f82330194dfa8d3/README.md#L137-L153), [wrapper boundary](https://github.com/Bridge-Node-7/frontier-intelligence-workflows/blob/36366e96c12765e14d09965c1f82330194dfa8d3/scripts/validate_repo.py#L206-L216), [scanner resolves the root](https://github.com/Bridge-Node-7/frontier-intelligence-workflows/blob/36366e96c12765e14d09965c1f82330194dfa8d3/scripts/release_common.py#L226-L230), and [lexical comparison](https://github.com/Bridge-Node-7/frontier-intelligence-workflows/blob/36366e96c12765e14d09965c1f82330194dfa8d3/scripts/validate_repo_core.py#L572-L577).

[Python's pathlib documentation](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.relative_to) distinguishes lexical relative paths from filesystem resolution. Canonicalize the existing root boundary rather than suppressing the exception or weakening file-policy checks. See [T04](TODO.md#t04).

## F05

**P2 · FMA accepts explicit null criticality, then rejects the same graph in coverage.** Confirmed early-validation discrepancy.

A graph with a single claim node and `criticality: null` passes the actual `fma validate` CLI with exit 0. `fma coverage` over the same file exits 2 because null cannot be converted to a float. The CLI controls that error; this is not a traceback or security finding. The published graph schema requires a numeric value from 0 through 5 when criticality is present.

Evidence: [numeric contract](https://github.com/Bridge-Node-7/frontier-mission-assurance/blob/f99dd2174c74f26b648321e02f8d30e2cff10230/schemas/assurance-graph.schema.json#L67-L70), [validator skips null](https://github.com/Bridge-Node-7/frontier-mission-assurance/blob/f99dd2174c74f26b648321e02f8d30e2cff10230/src/frontier_assurance/validate.py#L126-L135), [coverage conversion](https://github.com/Bridge-Node-7/frontier-mission-assurance/blob/f99dd2174c74f26b648321e02f8d30e2cff10230/src/frontier_assurance/analysis.py#L29-L35), and [CLI contract](https://github.com/Bridge-Node-7/frontier-mission-assurance/blob/f99dd2174c74f26b648321e02f8d30e2cff10230/docs/CLI_CONTRACT.md#L9-L20).

Minimal synthetic input:

```json
{"graph_version":"1.0","nodes":[{"id":"CLAIM-NULL","kind":"claim","title":"Synthetic null criticality","status":"open","criticality":null}],"edges":[]}
```

Reject an explicitly invalid value at graph validation while retaining omission semantics. Turning null into zero downstream would conceal the bad input. [JSON Schema type semantics](https://json-schema.org/draft/2020-12/json-schema-validation#section-6.1.1) distinguish null and number. FMA is proprietary evaluation/review software with a maintainer-only contribution policy; this review supplies a specification rather than a source patch. See [T05](TODO.md#t05).

## F06

**P2 · Pax Silica's eligibility verification exceeds its published snapshot boundary.** Confirmed chronology and field-validation gaps.

The published corpus boundary is September 29, 2026, while a program's `eligibility_verified_at` is September 30. The README defines the corpus date as the review boundary. The validator checks generic verification dates and source IDs but omits the eligibility-specific fields. The full existing gate passes, and the generator copies that canonical JSON into the public distribution.

Disposable variants show that malformed eligibility dates/source fields are accepted as well. The refined candidate rejects 38 invalid variants and the published chronology contradiction, while preserving seven valid/optional controls. Its 62-test full gate was verified with an explicitly synthetic in-boundary date in a disposable copy; that date is **not** a factual correction. The unchanged published record intentionally fails under the stricter candidate until its owner resolves the chronology. Optional pairing and minimum-array policy are not declared by the existing contract and remain owner decisions. [Verification](evidence/pax-eligibility-validation.json) records exact outcomes and byte-unchanged actual data.

Evidence: [corpus-boundary definition](https://github.com/Bridge-Node-7/pax-silica/blob/2f62f678d06f8444ddc7788ce03e1f1f46cf4cba/README.md#L28), [snapshot date](https://github.com/Bridge-Node-7/pax-silica/blob/2f62f678d06f8444ddc7788ce03e1f1f46cf4cba/data/pax-silica.json#L4-L6), [eligibility fields](https://github.com/Bridge-Node-7/pax-silica/blob/2f62f678d06f8444ddc7788ce03e1f1f46cf4cba/data/pax-silica.json#L478-L483), [generic date enforcement](https://github.com/Bridge-Node-7/pax-silica/blob/2f62f678d06f8444ddc7788ce03e1f1f46cf4cba/scripts/validate_data.py#L322-L347), and [public data generation](https://github.com/Bridge-Node-7/pax-silica/blob/2f62f678d06f8444ddc7788ce03e1f1f46cf4cba/scripts/build_web.py#L265-L266).

The [official grant detail page](https://simpler.grants.gov/opportunity/2f434e81-c476-49bb-a7e6-9a320c907cd9) supports the reviewed eligibility category; no category-inaccuracy finding is made. Its direct URL is a useful replacement for the current search locator within the same correction. The evidence owner must establish the actual date and intended boundary. See [T06](TODO.md#t06).

## F07

**P2 · The recommended quantum worked example differs from its current readiness rubric.** Confirmed instructional inconsistency, with a coverage traceability limitation.

The README recommends the completed fictional Decision Pack as the first example. Its ten readiness rows omit the current method's **Critical-link protection** and **Crypto-agility architecture** domains and substitute other labels without a mapping or tailoring rationale. Earlier single-file examples redirect to this pack, so the discrepancy is not a declared legacy example.

Evidence: [recommended entry point](https://github.com/Bridge-Node-7/quantum-readiness-space-communications/blob/0f926377de268b20c2b1223eaf830405b8eb3648/README.md#L17-L23), [canonical domains/template](https://github.com/Bridge-Node-7/quantum-readiness-space-communications/blob/0f926377de268b20c2b1223eaf830405b8eb3648/assessment/migration-readiness-profile.md#L22-L75), [worked profile](https://github.com/Bridge-Node-7/quantum-readiness-space-communications/blob/0f926377de268b20c2b1223eaf830405b8eb3648/examples/sample-small-satellite-decision-pack/04-migration-readiness-profile.md#L5-L14), and [coverage method](https://github.com/Bridge-Node-7/quantum-readiness-space-communications/blob/0f926377de268b20c2b1223eaf830405b8eb3648/assessment/evidence-confidence-ledger.md#L44-L52).

The associated example reports 64% coverage from 7 of 11 items. The rounding is correct, but the pack supplies neither an approved eleven-item counting unit nor evidence that seven scope items are complete. Seven evidence-ledger IDs do not establish seven complete items, particularly where support is stale, conflicting or incomplete. This belongs in the same worked-example correction, not a separate severity claim.

The verified correction uses the canonical domains and makes coverage `NOT_ESTABLISHED` consistently in the existing coverage and decision records. Eight scope/dependency, ten domain and twelve critical-condition traces expose evidence limits and overlap; they are not an approved denominator. The original ledger, fictional posture and open conditions remain unchanged. [Candidate verification](evidence/quantum-example-traceability.json) distinguishes manual semantic review from the passing offline gate. [NIST's crypto-agility guidance](https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final) supports the architectural concern, but does not validate this rubric's stages. [RFC 9954](https://www.rfc-editor.org/info/rfc9954/) provides informational hybrid-TLS considerations, not a mission-specific prescription. See [T07](TODO.md#t07).

## Baseline strengths and verification limits

- All eight public repositories were inventoried, including the profile and the FIW template. None was archived or a fork. The terminal second API page was empty. The `BridgeNode7` organization has no public repositories and points to the canonical `Bridge-Node-7` account.
- Recent inspected-head validation/CI runs were successful across all eight repositories. Local probes exercise gaps outside those passing suites. Local original-source gates passed for FMA, ACA, M2M, Pax, and Quantum; FIW failed as described in F04. FDE's unit tests passed, but its full unchanged-source gate encountered repeated context-handoff/module-load failures. Subsequent controlled probes isolated a single-threaded local test-server blockage; only the separately corrected harness plus timestamp proposal passes the current complete candidate gate.
- The bounded link check extracted 556 inline Markdown links and found no missing local or mapped cross-repository `main` path targets. Six checked first-party company URLs returned HTTP 200. Markdown fragments, rendered accessibility, all external sources, and deployed/source byte parity were not comprehensively verified.
- Public examples and limitations consistently distinguish synthetic/public-source evidence from qualification, scientific truth, and accountable human decisions. Source versions ahead of stable releases are explicitly labelled intentional/unreleased. These are appropriate boundaries, not missing company capability.
- Quantum's offline gate passed; its external-link checker encountered an NSA automated-access HTTP 403. Independent web reading reached the source. This is an access limitation, not a confirmed dead link. Research checks were selective and do not independently re-establish every Pax source or frontier-science claim.
- Primary-source research used official Python/JSON Schema documentation, the existing interoperability contracts, selected NIST publications, IETF material, and the official grant listing. No recommendation requires a new scoring engine, governance framework, runtime service, AI model, or broader repository architecture.

No private Bridge Node 7 repository, credentialed vendor system, real protected case, production deployment, customer workload, or scientific/mission qualification was evaluated. Stable release assets and their attestations were inspected as metadata; their download bytes were not independently verified. All candidate changes remain independent proposals against the recorded source bases.
