# Academic Claim Discipline Skill

Use this skill before converting exploratory ideas into manuscript text.

## Goal

Prevent academic slop, overclaiming, invented citations, and unsupported contribution statements.

## Quick Decision Tree

Classify in order of precedence (apply checks in order; use the first matching classification):

1. **Did we prove it ourselves in the paper?** → Proven in the paper
2. **Did we compute or simulate it?** → Computationally/simulation-supported
3. **Is it from a credible citation?** → Established by citation
4. **Is it plausible but unproven?** → Speculative
5. **Otherwise** → Unsupported

**Note:** If a claim fits multiple categories, classify it under the highest precedence category listed. If a claim cannot be classified due to insufficient context, flag it for manual review.

## Pre-submission checks

**Validation checks (support & precision):**
1. Is the claim precise and does wording match support?
2. Is it supported? If yes, what type?

**Communication checks (clarity & scope):**
3. Could it be misread as stronger than intended?
4. Does it require a citation?

**Conflict checks (context alignment):**
5. Does it conflict with `_context/current_issues.md`?

## Manuscript language by claim type

**Strong language** (proven or directly supported):
- "We prove that..."
- "The paper demonstrates..."

**Cautious language for simulation findings:**
- "In the design grid considered..."
- "The simulation suggests..."
- "Within this exercise..."
- "This pattern is consistent with..."

**Cautious language for speculative directions:**
- "A possible extension is..."
- "This suggests a connection to..."
- "This may provide a route toward..."

## Restricted words (use only when fully justified)

Avoid these unless the claim is proven or properly scoped:

| Word | When to avoid | Exception |
|------|---------------|-----------|
| "always" | Over-generalizes findings | Only for proven universals |
| "uniformly" | Implies universal consistency | Limited to proof contexts |
| "dominates" | Suggests unconditional superiority | Requires comprehensive comparison |
| "solves" | Claims problem resolution | Restrict to full solutions |
| "establishes" | Overstates simulation evidence | Use only for empirical proof |
| "novel" | Unverified uniqueness claims | After novelty verification |
| "robust to risk aversion" | Without probability foundation | Only if probability-based + precise |

## Output format

Use:

1. Proposed claim
2. Classification
3. Support
4. Risk
5. Safer wording
6. Whether citation/proof/simulation is needed