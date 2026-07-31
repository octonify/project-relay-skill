# Skill Benchmark: project-relay

**Model**: claude-opus-5
**Date**: 2026-07-30T16:34:19Z
**Evals**: 0, 1, 2 (1 runs each per configuration)

## Summary

| Metric | With Skill | Old Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 92% ± 3% | 87% ± 6% | +0.06 |
| Time | 183.9s ± 54.3s | 249.2s ± 97.9s | -65.3s |
| Tokens | 54454 ± 8087 | 57852 ± 10909 | -3397 |

## Notes

- Baseline here is the ITERATION-1 SKILL (snapshot), not the no-skill condition. This iteration answers 'did the revision help', not 'is the skill worth using'. The no-skill numbers from iteration-1 (90.7%) are not directly comparable - the assertion set grew from 14 to 18.
- Pass rate 92.3% (50/54) revised vs 86.7% (47/54) iteration-1 skill. The revised skill fixed session-narrative bleed and repeated-rationale on eval-1, and duplication/source-restatement on eval-2. Every remaining failure in the revised arm is a size-cap fail.
- Document size, revised vs iteration-1 skill, same conditions: eval-0 15,148 vs 21,085 (-28%); eval-1 16,172 vs 21,693 (-25%); eval-2 36,079 vs 61,836 (-42%).
- IMPORTANT CAVEAT on those size numbers: the iteration-1 skill produced 28,896 chars on eval-0 last round and 21,085 this round - 27% run-to-run variance on an identical skill and identical input. With n=1 per cell, the eval-0 delta (-28%) is inside that noise band and the eval-1 delta (-25%) is borderline. Only eval-2 (-42%, plus two additional assertion passes) is clearly beyond variance. Treat 'shrunk by a quarter' as unproven; 'shrunk on eval-2' as supported.
- The revised skill is also cheaper and faster: 54.5k vs 57.9k tokens (-6%) and 184s vs 249s (-26%). Less output to generate.
- No arm hit its size cap. Revised: 15,148 vs 12,000; 16,172 vs 14,000; 36,079 vs 20,000. Caps were set from iteration-1 output and were deliberately demanding.
- Root cause of residual bloat is structural, not stylistic - graders traced it to the section layout inviting restatement. On eval-0 the legacy freeze appears 4x, AUTH-214 4x, the TTL placeholder 5x, and sections 10-11 re-serialise 2-9. On eval-2 the risk register, constraints block, do-not-repeat list, next-action block and continuation-sources table each appear in BOTH documents. Next lever is cross-references and single-home rules for those blocks, not more instruction to be brief.
- EVAL BUG found by a grader: assertions 16 and 17 on eval-1 conflict. #17 rewards labelling unverified claims; the natural phrasing ('not verified this session') is what #16 penalises as session narrative. Both arms were scored against a contradiction. Reword before the next iteration.
- Scoring gradient is lopsided: 16-17 assertions reward presence, 1 penalises length. That is the same incentive that produces the redundancy being measured. eval-2's grader suggests replacing the similarity check with four mechanical single-home checks (does the risk register / constraints / do-not-repeat / next-action block appear in exactly one document).
- Uncovered fabrication hole: eval-2's no-fabrication assertion is scoped to git/build/CI, so it passed while the revised Master invented a source-precedence rule ('a written answer from Marcus beats the live website, which beats the pitch deck') that appears in no input. In a content project that is more dangerous than a fake commit hash.
- Both arms independently derived a real finding present in no source: brief.md contracts 8 pages and 6 cards while content-calendar.csv tracks only 4 and 2. No assertion credits it.