# Prioritized implementation TODO

All tasks are **open upstream**. Prepared patches are independent review candidates; they are not deployed fixes. Priority definitions, evidence, reproduced behavior, and primary references are in [FINDINGS.md](FINDINGS.md). [Proposal status](proposals/README.md) records the tested scope of each candidate.

Estimated maintainer implementation effort is **15–28 hours**, excluding optional macOS CI work, owner-response delays, release approvals, and production deployment. The first three tasks account for **8–16 hours**. These estimates assume an engineer familiar with the repository and an available declared toolchain. The separate external-review workload is in [WEEK_PLAN.md](WEEK_PLAN.md).

| Order | Task | Priority | Responsible role | Effort | Current preparation |
| --- | --- | --- | --- | --- | --- |
| 1 | [T01: Validate M2M source before FMA projection](#t01) | P1 | M2M maintainer | 2–4 h | Complete candidate locally and hosted verified; profile/version provenance included |
| 2 | [T02: Enforce FDE freshness date contract](#t02) | P1 | FDE maintainer; context-contract owner | 4–8 h | Supported-format candidate verified with separate context-server correction; leap-second policy remains |
| 3 | [T03: Bind ACA retests to the corrective action being closed](#t03) | P1 | ACA structured-case maintainer | 2–4 h | Complete candidate locally and hosted verified, including required CodeQL |
| 4 | [T04: Normalize FIW roots consistently](#t04) | P2 | FIW maintainer | 1–2 h | Reverified candidate, alias handling and deterministic package |
| 5 | [T05: Reject explicit null FMA criticality early](#t05) | P2 | FMA maintainer | 1–2 h | Evaluation-only bug specification |
| 6 | [T06: Correct and validate Pax eligibility provenance](#t06) | P2 | Source-data maintainer; evidence reviewer | 2–3 h | Typed/reference checks verified; full patch needs chronology-policy revision to preserve owner-intended data |
| 7 | [T07: Align the quantum worked example with its rubric](#t07) | P2 | PQC methodology maintainer; assessor | 3–5 h | Traceability correction verified; coverage NOT_ESTABLISHED pending owner decisions |

## T01

**Validate the authoritative M2M case before writing an FMA projection.** [Evidence and references: F01](FINDINGS.md#f01).

**Affected scope:** `materials-to-mission/scripts/export_fma_projection.py`, existing interoperability integration tests, and generated validation evidence. **Benefit:** users receive the same source-policy rejection through the export route as through the producer's validation route. **Priority rationale:** portable artifacts should not conceal known source-policy failure behind target-schema PASS.

Reuse the existing `validate_case` function with explicit public validation and the current default profile after the synthetic/public-safe declaration check. Raise an actionable error containing existing finding codes, paths, and messages before any output is written. Preserve the valid deterministic transformation, loss-aware extensions, pinned FMA contracts, and human-authority limitations. The candidate records the actual `ValidationResult.validation_profile` and toolkit `__version__` in the extensible graph metadata and manifest source fields, without changing schema or adapter versions.

**Acceptance:** the valid synthetic case still exports deterministically; all five checked-in invalid cases and the additional synthetic boundary-marker case exit nonzero before creating output; the valid graph/receipt remains usable under the pinned FMA contracts. After adaptation, refresh evidence with the repository's existing `check_repo.py --update-evidence` path, review the generated changes, and require a subsequent non-mutating full gate. The complete candidate passes 302 tests and four targeted CLI interoperability tests on Python 3.11.16; additional Python 3.12.14 and 3.13.15 gates each pass 302 tests, with the declared 3.12 consumer path also checked. The decision receipt is byte-identical to the valid baseline, and the unchanged FMA consumer accepts graph/reference checks. [Current verification](evidence/m2m-source-validation.json) preserves the existing consumer warning and exact limits; independent hosted verification now passes all four Ubuntu/Windows Python 3.11/3.13 maintainer cells (302 tests each), separate privacy/deterministic checks, and the Ubuntu Python 3.12 consumer path. Upstream acceptance remains open.

**Dependencies/access:** no new service or dependency. The semantic-profile identity is taken from the existing validation result, not inferred. The external reviewer has prepared the [candidate](proposals/m2m-source-validation.patch); interface acceptance, applying it upstream, required gates, and publishing require Bridge Node 7 maintainers.

## T02

**Enforce contract-valid freshness timestamps in FDE's context acceptance.** [Evidence and references: F02](FINDINGS.md#f02).

**Affected scope:** `frontier-decision-engine/site/src/lib/governed-context.js`, existing governed-context tests, and generated facts/manifest. **Benefit:** malformed expiry or review metadata cannot produce a CURRENT, active-eligible packet. **Priority rationale:** this directly affects context admitted into decision preparation.

Reject non-null deadlines when the parser cannot parse them. The candidate enforces types, RFC3339 lexical structure and Gregorian calendar bounds across `issued_at`, `source_as_of`, `review_due_at`, and `valid_until`, preserving valid offsets, lower-case separators and fractions. Make the supported format behavior explicit with the producer/consumer contract owner; do not silently coerce invalid values into absence or rewrite legacy packets. Native `Date` does not parse announced leap seconds and retains millisecond precision. The owner must document this supported subset or choose a deliberate leap-second policy before claiming complete RFC3339 acceptance.

**Acceptance:** valid supported date-time strings and allowed explicit null remain supported; wrong types, blanks, unparseable strings, parseable non-contract strings, and impossible dates are rejected with field-specific errors. Preserve current/review-due/expired/not-established, chronology, clock-skew, integrity, and legacy inspection behavior. Nineteen targeted tests exercise 104 malformed mutations, null rules and valid controls with actual packet digests. Refresh facts/manifest through existing commands, then require `npm run check` on the supported maintainer toolchain. With the separately disclosed context-server correction, the complete local gate passes 229 Node tests and all browser/release stages on Node 22.23.3 and 24.19.0. [Verification](evidence/fde-timestamp-contract.json) records supported tooling, raw-log hashes and remaining limits; independent Ubuntu Node 22 checks now pass the timestamp-only targeted/Node gates, harness-only context gate, and combined complete gate, including required Python and JavaScript CodeQL (zero reported results). Timestamp-only full browser behavior on Ubuntu was not tested or inferred.

**Dependencies/access:** no external provider is needed. The [timestamp candidate](proposals/fde-rfc3339-timestamp-contract.patch) alone passes targeted and Node tests but failed the full local macOS gate at the context browser handoff. Controlled probes identify preopened connections blocking the existing single-threaded local test server. The independent [native threaded-server correction](proposals/fde-context-threaded-harness.patch) passes the original context suite; both proposals together pass the full gate. Timestamp validation did not fix transport. Upstream implementation, repository-specific acceptance and the supported date-time policy need the FDE maintainer and contract owner.

**Owner decision:** will the context-contract owner document the runtime-supported subset, including rejection of announced leap seconds and millisecond comparisons, or require explicit leap-second/sub-millisecond handling? Supply the agreed producer/consumer contract and expected boundary examples before changing those semantics or claiming complete RFC3339 acceptance. [RFC3339 sections 5.6–5.7](https://www.rfc-editor.org/rfc/rfc3339.html#section-5.6) permit fractional seconds and valid announced leap seconds; they do not select FDE's comparison policy. Supported-runtime checks and the separate harness review can proceed without this answer.

## T03

**Require consistent finding → corrective action → retest closure links.** [Evidence and references: F03](FINDINGS.md#f03).

**Affected scope:** `ai-cyber-assurance/scripts/validate_assurance_case.py` and the existing real-validator fixture checks. **Benefit:** generated closed-finding views reflect a connected declared corrective-action path. **Priority rationale:** the documented machine-checkable closure relationship currently accepts contradictory records.

Require nonempty `finding_ref` and `corrective_action_ref` in retests. Keep existing typed reference resolution, compare the corrective action's finding to the retest's finding, and require a closed finding's successful retest action to be one of its recorded corrective actions. Preserve independent-retest rationale, chronology, completed-action, closure-evidence, and human-authority checks.

**Acceptance:** the original AI-agent and cryptographic examples still validate/render. Removing a retest's action link or linking it to another finding's action fails with retest/action/finding identifiers. Rendering invalid closure records stops before producing communication artifacts. The complete candidate passes 67 tests, 17 repository checks, and all 73 manifest hashes on Python 3.12.14. Twenty invalid synthetic variants fail before rendering output; both original examples and a correctly linked additional action pass. [Current verification](evidence/aca-closure-links.json) records actual CLI results and reproduction recipes. Independent hosted Ubuntu/Windows Python 3.12 jobs each pass 67 tests, 17 repository checks and 73 manifest hashes; required Ubuntu Python CodeQL completes with zero reported results. Three useful integration tests extend the existing suite; no new graph framework or runtime schema dependency is necessary.

**Dependencies/access:** no private case is needed to reproduce the issue. The external reviewer has prepared the [candidate](proposals/aca-closure-links.patch), including the required manifest hashes. Source implementation, metadata refresh after adaptation, and release approval require the ACA maintainer.

## T04

**Resolve FIW's repository root once before lexical path comparisons.** [Evidence and references: F04](FINDINGS.md#f04).

**Affected scope:** `frontier-intelligence-workflows/scripts/validate_repo.py`, `MANIFEST.sha256`, and `REPO_MANIFEST.json`. **Benefit:** macOS evaluators can execute the documented verification path and receive bounded negative-fixture results. **Priority rationale:** a small correction removes a reproduced platform failure without expanding the product.

Review the [candidate](proposals/fiw-canonical-root.patch), which adds the root-resolution line and required deterministic manifest updates. Confirm that canonicalization remains consistent with the existing scanner and containment policy. A focused macOS execution of the existing test/compile commands is justified by this observed failure; it is optional additional work, estimated at 1–2 hours, rather than a broad new platform matrix.

**Acceptance:** the unchanged alias-root reproduction succeeds after the correction; the existing 181 tests pass with zero errors/skips, compile checks pass, and both ordinary and actual alias-root validators report 20/20. Negative file-policy tests retain their existing meaning. All 133 manifest hashes, whitespace checks and repeated deterministic package checks pass at the exact source base. [Reverification](evidence/fiw-root-verification.json) records the commands and log hashes; generated test archives remain private cache artifacts.

**Dependencies/access:** macOS and declared validation dependencies; no service credentials. The external reviewer has prepared and locally validated the patch. Applying it and deciding whether to add the focused hosted smoke job require the FIW maintainer.

## T05

**Reject present-but-null FMA criticality at graph validation.** [Evidence and references: F05](FINDINGS.md#f05).

**Affected scope:** `frontier-mission-assurance/src/frontier_assurance/validate.py` and existing schema/CLI fixture checks. **Benefit:** the initial graph-validation result agrees with the downstream coverage command. **Priority rationale:** this produces a controlled later failure rather than an active misleading decision state, so it follows the source/record-integrity fixes.

Distinguish an omitted optional value from an explicitly invalid null. Enforce the existing numeric range and type semantics at validation; do not make coverage silently replace null with zero.

**Acceptance:** the minimal F05 graph fails `fma validate` with exit 2 and a node/field diagnostic. Omission, numeric 0, and numeric 5 remain accepted; Boolean and out-of-range values remain rejected. Coverage returns the same early validation error, and the existing 255-test `make check` gate passes. [Fourteen unchanged-source CLI calls](evidence/fma-criticality-specification.json) reproduce the null mismatch and valid/invalid controls. No candidate implementation or candidate full-gate result is asserted.

**Dependencies/access:** FMA's evaluation/review rights and contribution policy apply. The external reviewer can provide the original synthetic input and specification; only the FMA maintainer should implement the source change. No proprietary patch is included and no additional runtime dependency is proposed.

## T06

**Validate Pax eligibility fields while preserving the owner's separate field-review date.** [Evidence and references: F06](FINDINGS.md#f06).

**Affected scope:** `pax-silica/scripts/validate_data.py`, existing validator tests and the eligibility-field contract. **Benefit:** malformed dates and orphan eligibility references receive explicit diagnostics without rejecting intentionally separate field freshness. **Priority rationale:** the eligibility-specific fields currently bypass the established type/reference conventions.

Owner-authored merged [PR #50](https://github.com/Bridge-Node-7/pax-silica/pull/50) records the September 30 eligibility review while deliberately retaining the September 29 full-snapshot boundary from PR #48. The specific date/boundary intent is resolved. Do not backdate the field or advance the overall snapshot to satisfy the review's stricter candidate.

**Acceptance:** present eligibility dates must be canonical real `YYYY-MM-DD` strings; present source fields must be arrays of nonempty resolved IDs. Malformed values and orphan IDs must fail with program/field diagnostics. Preserve independent omission and empty arrays unless the owner approves a stricter contract. Remove or narrow the candidate's global-cutoff guard consistently with PR #50; then require the existing full gate on unchanged actual data, deterministic generation, and affected browser behavior if publication-facing behavior changes. Additional chronology restrictions need an explicit eligibility-field contract rather than inference from generic `verified_at`.

**Candidate disposition:** **REQUIRES_CHRONOLOGY_POLICY_REVISION_BEFORE_ADOPTION**. The [preserved patch](proposals/pax-eligibility-validation.patch) rejects owner-intended data. Its prior 38 rejected probes include the disputed date rule; seven controls and a synthetic 62-test full gate passed. These are historical execution results, not acceptance evidence for that rule. This phase preserves the patch and original evidence; it does not claim a revised Pax candidate or actual-data full-gate pass. [Verification](evidence/pax-eligibility-validation.json) records the owner sources and exact limits.

**Dependencies/access:** the Pax maintainer must revise and accept the candidate under the intended field contract. The owner still decides any pairing/minimum-source or additional chronological requirements, and must preserve truthful review/locator history if replacing S-06 with the official detail URL. PR #50 establishes declared review intent, not independent factual attestation of the source capture. The published data needs no inferred date repair; implementation and release acceptance remain open.

## T07

**Make the current quantum Decision Pack teach its canonical readiness method.** [Evidence and references: F07](FINDINGS.md#f07).

**Affected scope:** the existing sample pack's `04-migration-readiness-profile.md`, `05-evidence-confidence-and-coverage.md`, one necessary matching sentence in `10-decision-record-and-review.md`, and generated manifests. **Benefit:** a new assessor can follow the canonical method and see unsupported completeness/coverage claims. **Priority rationale:** correct the worked example before adding research features or scoring logic.

Use the canonical ten-domain template, including Critical-link protection and Crypto-agility architecture. Map existing fictional observations into the appropriate domains and retain Not Assessed where evidence is absent or stale. The current pack does not establish seven complete items or an approved eleven-item denominator. The candidate makes coverage `NOT_ESTABLISHED` and provides eight scope/dependency, ten domain-claim and twelve critical-condition traces with references and limitations. These overlapping registers must not be summed. The original seven-record ledger, critical posture and pending approval remain unchanged.

**Acceptance:** an independent assessor can trace every canonical domain/stage and declared critical condition to fictional evidence or an explicit limitation. The complete offline gate passes 50 existing tests, 93 hashes, links and deterministic packaging on Python 3.12.14. [Verification](evidence/quantum-example-traceability.json) separates those checks from manual semantic review. Coverage remains `NOT_ESTABLISHED` until approved counting units, claim-specific support floors and current applicable evidence justify a numerator/denominator and rounding. No evidence is invented, condition closed or deployment authorized; no static wording test, spreadsheet or scoring engine is added.

**Dependencies/access:** the [candidate](proposals/quantum-example-traceability.patch) is prepared and verified. The methodology owner must approve complete scope/counting units, support floors, currency/applicability review and the remaining conflict/unknown/closure decisions before establishing coverage. Publishing or changing methodology requires Bridge Node 7 maintainers. No real mission data is needed for this fictional correction; NIST/IETF context informs applicability, not endorsement.

**Owner decision:** the PQC methodology maintainer/assessor must provide approved scope and counting units, claim-to-item mapping with overlap resolved, claim-specific support floors, and the current applicability/conflict/unknown review. Those records determine completeness and any coverage numerator/denominator. The eight/ten/twelve trace registers cannot supply that approval or be summed. Canonical-domain and reference review can proceed independently while coverage remains `NOT_ESTABLISHED` and conditions remain open.

## Ownership and publication state

The review author can complete evidence preparation and proposed changes without upstream permissions. Every upstream task remains open until the responsible maintainer accepts and implements it with the stated checks. An unanswered internal question is recorded as a dependency, not converted into a company deficiency.

The report and its candidates are published on the public review repository's `codex/technical-review` branch under the user's explicit authorization to leave it public and continue commits and pushes. Upstream implementation remains open. The public branch link is ready for the user to share with the CEO.
