# Prioritized implementation TODO

All tasks are **open upstream**. Prepared patches are private, uncommitted candidates; they are not deployed fixes. Priority definitions, evidence, reproduced behavior, and primary references are in [FINDINGS.md](FINDINGS.md). [Proposal status](proposals/README.md) records the tested scope of each candidate.

Estimated maintainer implementation effort is **15–28 hours**, excluding optional macOS CI work, owner-response delays, release approvals, and production deployment. The first three tasks account for **8–16 hours**. These estimates assume an engineer familiar with the repository and an available declared toolchain. The separate external-review workload is in [WEEK_PLAN.md](WEEK_PLAN.md).

| Order | Task | Priority | Responsible role | Effort | Current preparation |
| --- | --- | --- | --- | --- | --- |
| 1 | [T01: Validate M2M source before FMA projection](#t01) | P1 | M2M maintainer | 2–4 h | Locally tested candidate |
| 2 | [T02: Enforce FDE freshness date contract](#t02) | P1 | FDE maintainer; context-contract owner | 4–8 h | Partial candidate tested; date-format work remains |
| 3 | [T03: Bind ACA retests to the corrective action being closed](#t03) | P1 | ACA structured-case maintainer | 2–4 h | Reproductions and correction specification |
| 4 | [T04: Normalize FIW roots consistently](#t04) | P2 | FIW maintainer | 1–2 h | Locally tested candidate with refreshed manifests |
| 5 | [T05: Reject explicit null FMA criticality early](#t05) | P2 | FMA maintainer | 1–2 h | Evaluation-only bug specification |
| 6 | [T06: Correct and validate Pax eligibility provenance](#t06) | P2 | Source-data maintainer; evidence reviewer | 2–3 h | Validator candidate tested; factual date unresolved |
| 7 | [T07: Align the quantum worked example with its rubric](#t07) | P2 | PQC methodology maintainer; assessor | 3–5 h | Focused update specification |

## T01

**Validate the authoritative M2M case before writing an FMA projection.** [Evidence and references: F01](FINDINGS.md#f01).

**Affected scope:** `materials-to-mission/scripts/export_fma_projection.py`, existing interoperability integration tests, and generated validation evidence. **Benefit:** users receive the same source-policy rejection through the export route as through the producer's validation route. **Priority rationale:** portable artifacts should not conceal known source-policy failure behind target-schema PASS.

Reuse the existing `validate_case` function with explicit public validation and the current default profile after the synthetic/public-safe declaration check. Raise an actionable error containing existing finding codes, paths, and messages before any output is written. Preserve the valid deterministic transformation, loss-aware extensions, pinned FMA contracts, and human-authority limitations. Record the source validation profile in projection provenance during the final interface review; a target schema version alone does not identify semantic acceptance.

**Acceptance:** the valid synthetic case still exports deterministically; all six checked-in invalid cases and the synthetic boundary-marker case exit nonzero before creating output; the valid graph/receipt remains usable under the pinned FMA contracts. Refresh evidence with the repository's existing `check_repo.py --update-evidence` path, review the generated changes, and require a subsequent non-mutating full gate. The candidate already passes 301 tests, but profile-provenance recording remains a final-review item.

**Dependencies/access:** no new service or dependency; confirm the semantic-profile identity with the maintainer. The external reviewer can prepare/replay the [candidate](proposals/m2m-source-validation.patch); applying it, refreshing upstream evidence, and publishing require Bridge Node 7 maintainers.

## T02

**Enforce contract-valid freshness timestamps in FDE's context acceptance.** [Evidence and references: F02](FINDINGS.md#f02).

**Affected scope:** `frontier-decision-engine/site/src/lib/governed-context.js`, existing governed-context tests, and generated facts/manifest. **Benefit:** malformed expiry or review metadata cannot produce a CURRENT, active-eligible packet. **Priority rationale:** this directly affects context admitted into decision preparation.

First reject non-null deadlines when the existing parser cannot parse them. Complete runtime date-time validation consistent with the published contract across `issued_at`, `source_as_of`, `review_due_at`, and `valid_until`. Reuse existing validation patterns and make the supported format behavior explicit with the producer/consumer contract owner; do not silently coerce invalid values into absence or rewrite legacy packets.

**Acceptance:** valid date-time strings and allowed explicit null remain supported; wrong types, blanks, unparseable strings, parseable non-contract strings, and impossible dates are rejected with field-specific errors. Preserve current/review-due/expired/not-established, chronology, clock-skew, integrity, and legacy inspection behavior. Use actual packet digests in behavior checks. Refresh facts/manifest through existing commands, then require `npm run check` on the supported maintainer toolchain.

**Dependencies/access:** no external provider is needed. The [partial candidate](proposals/fde-nullable-date-guard.partial.patch) passes a full local candidate gate but still accepts `September 16, 2026`; do not close this task on that patch alone. The unchanged-source browser handoff failed intermittently in this audit; investigate/reproduce that separately rather than attributing its recovery to the timestamp fix. The external reviewer can prepare the candidate and contract probes; upstream implementation and acceptance need the FDE maintainer.

## T03

**Require consistent finding → corrective action → retest closure links.** [Evidence and references: F03](FINDINGS.md#f03).

**Affected scope:** `ai-cyber-assurance/scripts/validate_assurance_case.py` and the existing real-validator fixture checks. **Benefit:** generated closed-finding views reflect a connected declared corrective-action path. **Priority rationale:** the documented machine-checkable closure relationship currently accepts contradictory records.

Require nonempty `finding_ref` and `corrective_action_ref` in retests. Keep existing typed reference resolution, compare the corrective action's finding to the retest's finding, and require a closed finding's successful retest action to be one of its recorded corrective actions. Preserve independent-retest rationale, chronology, completed-action, closure-evidence, and human-authority checks.

**Acceptance:** the original AI-agent and cryptographic examples still validate/render. Removing a retest's action link or linking it to another finding's action fails with retest/action/finding identifiers. Rendering invalid closure records stops before producing communication artifacts. Existing 64 tests and metadata/hash/repository checks pass. Add only the useful real-validator behavior coverage for these missing relationships; no new graph framework or runtime schema dependency is necessary.

**Dependencies/access:** no private case is needed to reproduce the issue. The external reviewer can supply the two synthetic edits described in F03 and the correction specification; source implementation, metadata refresh, and release approval require the ACA maintainer.

## T04

**Resolve FIW's repository root once before lexical path comparisons.** [Evidence and references: F04](FINDINGS.md#f04).

**Affected scope:** `frontier-intelligence-workflows/scripts/validate_repo.py`, `MANIFEST.sha256`, and `REPO_MANIFEST.json`. **Benefit:** macOS evaluators can execute the documented verification path and receive bounded negative-fixture results. **Priority rationale:** a small correction removes a reproduced platform failure without expanding the product.

Review the [candidate](proposals/fiw-canonical-root.patch), which adds the root-resolution line and required deterministic manifest updates. Confirm that canonicalization remains consistent with the existing scanner and containment policy. A focused macOS execution of the existing test/compile commands is justified by this observed failure; it is optional additional work, estimated at 1–2 hours, rather than a broad new platform matrix.

**Acceptance:** the unchanged alias-root reproduction succeeds after the correction; the existing 181 tests pass with zero errors/skips, compile checks pass, and the ordinary validator reports 20/20. Negative file-policy tests retain their existing meaning. Manifest checks and diff checks pass at the exact source base.

**Dependencies/access:** macOS and declared validation dependencies; no service credentials. The external reviewer has prepared and locally validated the patch. Applying it and deciding whether to add the focused hosted smoke job require the FIW maintainer.

## T05

**Reject present-but-null FMA criticality at graph validation.** [Evidence and references: F05](FINDINGS.md#f05).

**Affected scope:** `frontier-mission-assurance/src/frontier_assurance/validate.py` and existing schema/CLI fixture checks. **Benefit:** the initial graph-validation result agrees with the downstream coverage command. **Priority rationale:** this produces a controlled later failure rather than an active misleading decision state, so it follows the source/record-integrity fixes.

Distinguish an omitted optional value from an explicitly invalid null. Enforce the existing numeric range and type semantics at validation; do not make coverage silently replace null with zero.

**Acceptance:** the minimal F05 graph fails `fma validate` with exit 2 and a node/field diagnostic. Omission, numeric 0, and numeric 5 remain accepted; Boolean and out-of-range values remain rejected. Coverage returns the same early validation error, and the existing 255-test `make check` gate passes.

**Dependencies/access:** FMA's evaluation/review rights and contribution policy apply. The external reviewer can provide the original synthetic input and specification; only the FMA maintainer should implement the source change. No proprietary patch is included and no additional runtime dependency is proposed.

## T06

**Repair the Pax eligibility chronology and enforce its existing provenance policy.** [Evidence and references: F06](FINDINGS.md#f06).

**Affected scope:** `pax-silica/data/pax-silica.json`, `scripts/validate_data.py`, and regenerated evidence/site artifacts. **Benefit:** the published cutoff and field-level source review agree, and orphan eligibility references cannot pass publication validation. **Priority rationale:** this is a specific published provenance inconsistency, not evidence that the program's eligibility category is wrong.

Have the evidence owner establish the actual eligibility review date and intended corpus boundary from the review record. Correct those fields only on that basis. Extend the existing source-ID and ISO-date/snapshot checks to `eligibility_source_ids` and `eligibility_verified_at`. Replace S-06's search locator with the verified official detail URL while reviewing that same record.

**Acceptance:** invalid dates, post-snapshot eligibility dates, and orphan eligibility sources fail. Settle the intended optional-field contract and explicitly check present-but-empty, null, and wrong-type values; the candidate does not yet establish exhaustive handling of those cases. The corrected canonical data and generated distribution preserve the supported eligibility category and source. The full 59-test gate, deterministic generation, and relevant browser behavior pass. Do not backdate evidence or advance the corpus boundary merely to make validation pass.

**Dependencies/access:** the [validator candidate](proposals/pax-eligibility-validation.patch) is tested but intentionally rejects the current published contradiction. Its positive full-gate test used a synthetic date fixture, not an evidence-backed data correction. The external reviewer can prepare/replay the validator; the source reviewer must supply the factual correction, and maintainers must publish it.

## T07

**Make the current quantum Decision Pack teach its canonical readiness method.** [Evidence and references: F07](FINDINGS.md#f07).

**Affected scope:** `quantum-readiness-space-communications/examples/sample-small-satellite-decision-pack/04-migration-readiness-profile.md` and `05-evidence-confidence-and-coverage.md`. **Benefit:** a new assessor can follow the recommended example without silently changing the published method. **Priority rationale:** correct the existing worked example before adding new research features or scoring logic.

Use the canonical ten-domain template, including Critical-link protection and Crypto-agility architecture. Map existing fictional observations into the appropriate domains, and retain explicit unknown/Not Assessed states where evidence is absent. In the existing coverage file, enumerate the fictional denominator items with stable IDs, applicable claim/evidence references, completeness rationale, and a counting rule; recompute the totals and rounding.

**Acceptance:** an independent assessor can trace every canonical domain and stage to fictional evidence or a stated unknown, reproduce the coverage numerator/denominator, and explain the retained critical-condition/non-authoritative posture. The existing complete validation and manifest/packaging gates pass. Human review assesses evidence adequacy; no static wording test, new spreadsheet, scoring engine, or operational cryptographic claim is needed.

**Dependencies/access:** review by the methodology owner or a qualified assessor; no real mission data is required. The external reviewer can draft the two-file correction privately. Publishing or changing the current methodology requires Bridge Node 7 maintainers. NIST/IETF context in F07 informs applicability, not endorsement of the rubric.

## Ownership and publication state

The private review author can complete evidence preparation and proposed changes without upstream permissions. Every upstream task remains open until the responsible maintainer accepts and implements it with the stated checks. An unanswered internal question is recorded as a dependency, not converted into a company deficiency.

The private GitHub repository has been created. This report and its candidates remain local and uncommitted until the user explicitly authorizes commits and pushes. CEO access requires a separately authorized collaborator invitation or another user-approved sharing method.
