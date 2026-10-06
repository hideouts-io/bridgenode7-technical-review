# Bridge Node 7 technical review

**Independent external assessment · Public review · Updated October 6, 2026**

The public GitHub estate already has substantial documentation, explicit evidence/authority limits, and successful recent hosted validation. This review recommends seven focused corrections to validation, source-policy enforcement, reproducibility, provenance, and an existing worked example. The strongest improvements reuse the code and methods already present.

All **eight public repositories** under the canonical [Bridge-Node-7 account](https://github.com/Bridge-Node-7) received a baseline assessment and exact commit identity. Focused implementation/methodology checks and local verification covered the seven project repositories; the profile's documented control-surface step was also run locally. This is a bounded public-source audit, not exhaustive verification of every source claim, private system, security property, or scientific result.

## Recommended decisions

**Next company action:** confirm accountable M2M and ACA maintainers to review T01 and T03 first, and name the FDE maintainer and context-contract owner to resolve T02's timestamp policy. The roles below are proposed; no assignment or upstream acceptance has been confirmed. The technical owner should record acceptance, rejection, or a specific deferral under the existing [TODO](TODO.md#ownership-and-publication-state).

| Order | Finding | Practical effect | Next action |
| --- | --- | --- | --- |
| 1 | [F01: M2M export bypasses source acceptance](FINDINGS.md#f01) | Source-policy failures can still become portable outputs. Target-schema PASS does not supply the missing source check. | M2M maintainer: review the runtime and default-profile documentation proposals together, then verify them at the accepted upstream commit. |
| 2 | [F03: ACA accepts disconnected closure links](FINDINGS.md#f03) | Closed-finding communication can be generated from inconsistent declared retest/action relationships. | ACA maintainer: review the required-link and closure-consistency candidate, then run the existing upstream acceptance checks. |
| 3 | [F02: FDE accepts malformed freshness dates](FINDINGS.md#f02) | Invalid expiry metadata can be labelled CURRENT and active-eligible. | FDE maintainer: review timestamp validation and the separate test-server correction. Contract owner: decide leap-second handling and comparison precision. |
| 4 | [F04: FIW verification fails on macOS aliases](FINDINGS.md#f04) | The documented local gate produces 32 errors from inconsistent path identity. | Review the tested one-line root correction and sealed-manifest updates. |
| 5 | [F05: FMA validates null criticality, then fails coverage](FINDINGS.md#f05) | Initial validation and downstream command behavior disagree. | Give the maintainer the minimal input and early-validation specification. |
| 6 | [F06: Pax eligibility fields bypass validation](FINDINGS.md#f06) | Field-specific checks are missing; the later eligibility review is intentional. | Review the revised candidate, verified locally and on Ubuntu/Windows with the owner-declared dates unchanged. |
| 7 | [F07: Quantum example differs from the current rubric](FINDINGS.md#f07) | The starting example omits two canonical domains and supplies no basis for its coverage totals. | Review the canonical-domain/traceability correction and approve counting/evidence rules before establishing coverage. |

These are tested local software/data observations and a documented example inconsistency. They do not demonstrate an operational compromise, an unauthorized human decision, or missing internal company capability. Priorities rank the proposed work within this review rather than assigning vulnerability severity.

**Current applicability, October 6:** M2M and FDE each advanced by one Pages-portability commit. Both unchanged proposal pairs pass textual application checks at the newer heads; their affected validation code remains unchanged. ACA remains at its reviewed base. Runtime gates were not rerun at the newer heads, and FDE's added Pages-portability CI stage must be included in maintainer acceptance. [Freshness evidence](evidence/verification.json) records the exact revisions and limits under `adoption_handoff`; prior test results remain bound to their original candidates.

## Start with the evidence

| Material | Purpose |
| --- | --- |
| [FINDINGS.md](FINDINGS.md) | Exact source links, triggers, observed results, research applicability, strengths, and limits. |
| [TODO.md](TODO.md) | Seven prioritized actions with responsible roles, access dependencies, effort, and measurable acceptance checks. |
| [WEEK_PLAN.md](WEEK_PLAN.md) | A proposed maintainer adoption week, with ownership, acceptance gates, and the original external-review estimate kept separate. |
| [inventory.csv](inventory.csv) | All repositories, purpose/audience, dependencies, inspected SHAs, docs/examples, tests, workflows, licenses, releases, relationships, and coverage limits. |
| [proposals/README.md](proposals/README.md) | Eight focused patches and an evaluation-only specification across seven tasks, exact source bases, tested scope, and remaining work. |
| [evidence/verification.json](evidence/verification.json) | Recorded local checks, captured hosted-run links, patch hashes, and raw-log provenance. |

Estimated maintainer implementation effort is **15–28 hours**, with **8–16 hours** for the first three tasks. That is separate from the external review plan and excludes owner-response delays, optional macOS CI work, release approvals, and deployment. No new dashboard, scoring model, broad framework, or additional public repository is justified by these findings.

## What the checks establish

FMA's 255 tests, ACA's 64 tests, M2M's 300-test complete gate, Pax's 59-test gate, and Quantum's 50-test offline gate passed on the inspected sources. M2M browser UAT and Pax Chromium UAT also passed. FIW's 181-test baseline had 32 errors; its candidate passed all 181 tests. FDE's 226 baseline Node tests passed, but its full unchanged-source gate failed at the context handoff. Controlled probes isolated a single-threaded local test-server blockage. The timestamp-only proposal still fails there on macOS; the separately corrected harness and timestamp proposal together pass the complete 229-test/browser gate on both Node 22.23.3 and 24.19.0.

The complete M2M and ACA candidates pass 302 and 67 tests respectively, with their existing metadata/repository gates. M2M's gate now covers the declared Python 3.11–3.13 minors locally, including the 3.12 consumer path. M2M rejects all five checked-in invalid cases plus a synthetic boundary sentinel before output; ACA rejects 20 invalid relationship variants before rendering. Those local macOS results retain their original scope; the separate hosted phase below verifies the required platform checks. FIW is reverified across alias handling and deterministic packaging. Pax's revised candidate passes all 62 tests on unchanged actual data, with 36 malformed variants rejected and eight valid/optional controls accepted. Its generated public files match the original source byte-for-byte; the separate field-review date intended by owner PR #50 is preserved. Independent Ubuntu/Windows Python 3.11/3.12 gates each pass 62 tests with identical public output across platforms. Quantum's 50-test offline gate passes, while its example coverage remains `NOT_ESTABLISHED` pending approved counting/evidence rules. These are candidate results, separate from unchanged-source baselines.

The [hosted candidate verification in the review repository](https://github.com/hideouts-io/bridgenode7-technical-review/actions/runs/37278630678) passed all ten jobs: M2M on Ubuntu/Windows with Python 3.11/3.13 plus its Ubuntu 3.12 consumer path; FDE's three separate Ubuntu Node 22 configurations; and ACA on Ubuntu/Windows with Python 3.12. FDE's combined gate and ACA's Ubuntu gate completed the required CodeQL languages with zero reported results, with candidate source bytes independently checked in the analysis databases. This closes the specified independent hosted verification gaps; upstream implementation, policy decisions and acceptance remain open. [Verification evidence](evidence/verification.json) records exact runners, versions, commands, results and setup corrections. The separate [Pax hosted verification](https://github.com/hideouts-io/bridgenode7-technical-review/actions/runs/37299070181) passes all seven jobs: four platform/Python cells, Python and JavaScript CodeQL analyses with zero reported results, and one aggregate status check. Its [evidence](evidence/pax-eligibility-validation.json) distinguishes local tests, hosted results and remaining upstream acceptance.

The navigation audit covers **300 tracked Markdown files, 598 links and one image** across the same eight source revisions. All 537 local or mapped GitHub file/directory occurrences resolve with exact path spelling, and the sole Markdown fragment matches its actual GitHub-rendered anchor. All 29 selected company/GitHub navigation URLs returned HTTP 200; no broken destination was confirmed.

The README-to-validation journey exposed one stale M2M default-profile sentence; a separate [T01 documentation companion](proposals/m2m-default-profile-doc.patch) corrects it and passes the 300-test local gate with required manifest verification. The unchanged runtime proposal and documentation companion also pass the [combined local 302-test gate](evidence/m2m-source-validation.json), with manifest, deterministic packaging and unchanged-file checks. This combined result is macOS arm64/Python 3.11.16 evidence; earlier hosted results cover the runtime proposal alone. Maintainer application and upstream acceptance remain open.

[Navigation evidence](evidence/verification.json) separates these results from earlier checks and excludes 37 unique third-party source URLs, email delivery, exhaustive browser/accessibility behavior and deployed/source byte parity. Quantum's network checker received an automated NSA HTTP 403 despite independent web access; it is an access limitation, not a confirmed broken reference. Public source/release differences are expressly documented as intentional, so this review does not turn them into backlog items.

Owner decisions remain for FDE's supported date-time policy, any additional Pax chronology/optional-field requirements and locator changes, and Quantum's approved scope, counting units and evidence support floors. These are stated dependencies, not assumed company deficiencies. FMA's evaluation-only rights and maintainer contribution policy are respected by providing an original-input specification rather than a proprietary source patch.

## Scope, tools, and sharing state

The [profile's canonical-source statement](https://github.com/Bridge-Node-7/Bridge-Node-7/blob/3f959138f3252b16bc69dabf178bdde83a606a3b/README.md#L74-L83) identifies `Bridge-Node-7` and [BridgeNode7.com](https://bridgenode7.com/). GitHub reports that account as a **User**. The similarly named `BridgeNode7` organization points to it and has zero public repositories. Complete pagination found eight repositories, no forks or archived repositories, and one template.

Research used the authenticated GitHub CLI/public API, public Git clones, native web research of primary sources, and existing project validation tools in isolated local environments. The GitHub plugin was not connected during the original audit; its connected metadata, targeted public-issue search, workflow-job and log tools were used during continuation. Authenticated GitHub Actions runs used only this review repository; official pinned CodeQL action sources resolved configuration questions. Dependencies stayed in isolated local environments or disposable runner environments. Research was selective; no internal or credentialed Bridge Node 7 systems were accessed.

The review is published in the public [hideouts-io/bridgenode7-technical-review repository](https://github.com/hideouts-io/bridgenode7-technical-review/tree/codex/technical-review), on `codex/technical-review`. The user explicitly authorized leaving it public and continuing focused commits and pushes. Current public visibility is verified; the reviewer did not change repository visibility. No upstream Bridge Node 7 repository was changed, and no issue, pull request, collaborator invitation, or CEO message was sent.

The public review link can be shared with the CEO without a collaborator invitation. This assessment is independent and does not imply official Bridge Node 7 sponsorship.
