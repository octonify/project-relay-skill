# Skill Benchmark: project-relay

**Model**: claude-opus-5
**Date**: 2026-07-30T14:18:33Z
**Evals**: 0, 1, 2 (1 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 91% ± 11% | +0.09 |
| Time | 271.0s ± 68.3s | 136.3s ± 13.0s | +134.7s |
| Tokens | 59440 ± 8546 | 37468 ± 2875 | +21972 |

## Notes

- Pass rate 100% (42/42) with skill vs 90.7% (38/42) without. The entire gap is structural assertions - file naming, canonical location, version fields, the two-document split. Zero factual-capture assertions separated the arms.
- The baseline is a strong fact-capturer. Unaided runs independently caught the planted traps in all three evals (untested code, rate-limit failure reason, unknown staging state, verbal-only offer, dead loyalty terms) and refused to fabricate contacts or git state. The skill's measured value is continuity plumbing, not diligence.
- eval-1 (master-cumulative-update) is non-discriminating: 14/14 in both arms. The fixture hands the baseline a well-structured v2.0 Master to imitate, so update-in-place evals leak the format for free. Treat its delta as uninformative rather than as evidence the skill does nothing.
- eval-2 (full-nontechnical-handover) is the only real discriminator: 14/14 vs 11/14. All three baseline failures were structural - root-level HANDOVER.md/NEXT-STEPS.md instead of dated files in docs/handoffs/, no version field anywhere, and no single designated next action. Cold-start evals discriminate; update evals do not.
- Cost is the clearest downside: 271s vs 136s (2.0x) and 59.4k vs 37.5k model tokens (1.6x). Output size is worse than the token delta suggests - eval-2 with-skill emitted ~60KB across two documents for a four-file content project, and eval-0 emitted ~29KB for a 78-line transcript. A continuity doc that outweighs the material it replaces undermines its own purpose. This is the top defect candidate for iteration 2.
- Assertion coverage gaps flagged independently by four of six graders: nothing penalizes fabrication (a run inventing a plausible commit hash would still score 14/14 on eval-1); nothing checks division of labour between Daily and Master (a Daily that duplicates the Master passes); and nothing credits catching stale inherited claims, which every with-skill run did (phantom handoff file, wrong commit, non-existent signup.ts, 'tests passing' with no tests).
- with_skill stddev is 0.00 on pass rate, but n=1 per eval - that is an artifact of single runs, not evidence of stability. Do not read it as low variance.
- One uncaught quality slip in the baseline eval-2 output: menu page labelled 'due Thu 31 Jul' when 31 July 2026 is a Friday. No assertion checks derived dates.