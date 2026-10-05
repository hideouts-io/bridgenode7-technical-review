# Bridge Node 7 technical review

**Independent external assessment · Public review · Updated October 5, 2026**

The public GitHub estate already has substantial documentation, explicit evidence/authority limits, and successful recent hosted validation. This review recommends seven focused corrections to validation, source-policy enforcement, reproducibility, provenance, and an existing worked example. The strongest improvements reuse the code and methods already present.

All **eight public repositories** under the canonical [Bridge-Node-7 account](https://github.com/Bridge-Node-7) received a baseline assessment and exact commit identity. Focused implementation/methodology checks and local verification covered the seven project repositories; the profile's documented control-surface step was also run locally. This is a bounded public-source audit, not exhaustive verification of every source claim, private system, security property, or scientific result.

## Recommended decisions

| Order | Finding | Practical effect | Next action |
| --- | --- | --- | --- |
| 1 | [F01: M2M export bypasses source acceptance](FINDINGS.md#f01) | Source-policy failures can still become portable outputs. Target-schema PASS does not supply the missing source check. | Review the complete source-preflight and profile/version-provenance candidate. |
| 2 | [F02: FDE accepts malformed freshness dates](FINDINGS.md#f02) | Invalid expiry metadata can be labelled CURRENT and active-eligible. | Review supported-format validation and the separate test-server correction; decide the leap-second policy. |
| 3 | [F03: ACA accepts disconnected closure links](FINDINGS.md#f03) | Closed-finding communication can be generated from inconsistent declared retest/action relationships. | Review the complete required-link and closure-consistency candidate. |
| 4 | [F04: FIW verification fails on macOS aliases](FINDINGS.md#f04) | The documented local gate produces 32 errors from inconsistent path identity. | Review the tested one-line root correction and sealed-manifest updates. |
| 5 | [F05: FMA validates null criticality, then fails coverage](FINDINGS.md#f05) | Initial validation and downstream command behavior disagree. | Give the maintainer the minimal input and early-validation specification. |
| 6 | [F06: Pax eligibility review exceeds its snapshot](FINDINGS.md#f06) | Published provenance contradicts the corpus cutoff, and field-specific checks are incomplete. | Have the evidence owner resolve the actual date; review the validator candidate. |
| 7 | [F07: Quantum example differs from the current rubric](FINDINGS.md#f07) | The starting example omits two canonical domains and supplies no basis for its coverage totals. | Review the canonical-domain/traceability correction and approve counting/evidence rules before establishing coverage. |

These are tested local software/data observations and a documented example inconsistency. They do not demonstrate an operational compromise, an unauthorized human decision, or missing internal company capability. Priorities rank the proposed work within this review rather than assigning vulnerability severity.

## Start with the evidence

| Material | Purpose |
| --- | --- |
| [FINDINGS.md](FINDINGS.md) | Exact source links, triggers, observed results, research applicability, strengths, and limits. |
| [TODO.md](TODO.md) | Seven prioritized actions with responsible roles, access dependencies, effort, and measurable acceptance checks. |
| [WEEK_PLAN.md](WEEK_PLAN.md) | A seven-day, 28-hour external investigation/preparation plan with achievable deliverables. |
| [inventory.csv](inventory.csv) | All repositories, purpose/audience, dependencies, inspected SHAs, docs/examples, tests, workflows, licenses, releases, relationships, and coverage limits. |
| [proposals/README.md](proposals/README.md) | Seven focused patches, an evaluation-only specification, exact source bases, tested scope, and remaining work. |
| [evidence/verification.json](evidence/verification.json) | Recorded local checks, captured hosted-run links, patch hashes, and raw-log provenance. |

Estimated maintainer implementation effort is **15–28 hours**, with **8–16 hours** for the first three tasks. That is separate from the external review plan and excludes owner-response delays, optional macOS CI work, release approvals, and deployment. No new dashboard, scoring model, broad framework, or additional public repository is justified by these findings.

## What the checks establish

FMA's 255 tests, ACA's 64 tests, M2M's 300-test complete gate, Pax's 59-test gate, and Quantum's 50-test offline gate passed on the inspected sources. M2M browser UAT and Pax Chromium UAT also passed. FIW's 181-test baseline had 32 errors; its candidate passed all 181 tests. FDE's 226 baseline Node tests passed, but its full unchanged-source gate failed at the context handoff. Controlled probes isolated a single-threaded local test-server blockage. The timestamp-only proposal still fails there on macOS; the separately corrected harness and timestamp proposal together pass the complete 229-test/browser gate on both Node 22.23.3 and 24.19.0.

The complete M2M and ACA candidates pass 302 and 67 tests respectively, with their existing metadata/repository gates. M2M's gate now covers the declared Python 3.11–3.13 minors locally, including the 3.12 consumer path. M2M rejects all five checked-in invalid cases plus a synthetic boundary sentinel before output; ACA rejects 20 invalid relationship variants before rendering. Those local macOS results retain their original scope; the separate hosted phase below verifies the required platform checks. FIW is reverified across alias handling and deterministic packaging. Pax's 62-test positive gate uses an explicitly synthetic date; unchanged actual data fails the stricter validator. Quantum's 50-test offline gate passes, while its example coverage remains `NOT_ESTABLISHED` pending approved counting/evidence rules. These are candidate results, separate from unchanged-source baselines.

The [hosted candidate verification in the review repository](https://github.com/hideouts-io/bridgenode7-technical-review/actions/runs/37278630678) passed all ten jobs: M2M on Ubuntu/Windows with Python 3.11/3.13 plus its Ubuntu 3.12 consumer path; FDE's three separate Ubuntu Node 22 configurations; and ACA on Ubuntu/Windows with Python 3.12. FDE's combined gate and ACA's Ubuntu gate completed the required CodeQL languages with zero reported results, with candidate source bytes independently checked in the analysis databases. This closes the specified independent hosted verification gaps; upstream implementation, policy decisions and acceptance remain open. [Verification evidence](evidence/verification.json) records exact runners, versions, commands, results and setup corrections.

The bounded Markdown check found no missing targets in **556 extracted inline links**; six checked company URLs returned HTTP 200. Fragments and all external sources were not exhaustively checked. Quantum's network checker received an automated NSA HTTP 403 despite independent web access; it is an access limitation, not a confirmed broken reference. Public source/release differences are expressly documented as intentional, so this review does not turn them into backlog items.

Owner decisions remain for FDE's supported date-time policy, Pax's factual provenance and optional-field contract, and Quantum's approved scope, counting units and evidence support floors. These are stated dependencies, not assumed company deficiencies. FMA's evaluation-only rights and maintainer contribution policy are respected by providing an original-input specification rather than a proprietary source patch.

## Scope, tools, and sharing state

The [profile's canonical-source statement](https://github.com/Bridge-Node-7/Bridge-Node-7/blob/3f959138f3252b16bc69dabf178bdde83a606a3b/README.md#L74-L83) identifies `Bridge-Node-7` and [BridgeNode7.com](https://bridgenode7.com/). GitHub reports that account as a **User**. The similarly named `BridgeNode7` organization points to it and has zero public repositories. Complete pagination found eight repositories, no forks or archived repositories, and one template.

Research used the authenticated GitHub CLI/public API, public Git clones, native web research of primary sources, and existing project validation tools in isolated local environments. The GitHub plugin was not connected during the original audit; its connected metadata, targeted public-issue search, workflow-job and log tools were used during continuation. Authenticated GitHub Actions runs used only this review repository; official pinned CodeQL action sources resolved configuration questions. Dependencies stayed in isolated local environments or disposable runner environments. Research was selective; no internal or credentialed Bridge Node 7 systems were accessed.

The review is published in the public [hideouts-io/bridgenode7-technical-review repository](https://github.com/hideouts-io/bridgenode7-technical-review/tree/codex/technical-review), on `codex/technical-review`. The user explicitly authorized leaving it public and continuing focused commits and pushes. Current public visibility is verified; the reviewer did not change repository visibility. No upstream Bridge Node 7 repository was changed, and no issue, pull request, collaborator invitation, or CEO message was sent.

The public review link can be shared with the CEO without a collaborator invitation. This assessment is independent and does not imply official Bridge Node 7 sponsorship.
