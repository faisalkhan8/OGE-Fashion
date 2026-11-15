# Research Questions and Operational Definitions
**Version:** 0.1 — proposed, pending literature and dataset review.

## RQ1 — Ontology representation
How can a shared ontology represent fashion, makeup, user preferences, attributes, and compatibility relationships in a machine-readable way?

**Evidence:** competency-question coverage; ontology consistency/reasoner checks; class/property coverage against catalogue metadata; documentation of unsupported concepts.

**Candidate indicators:** fraction of competency questions answerable; unsatisfiable classes/consistency errors; completeness of required catalogue attributes.

## RQ2 — Hybrid recommendation quality
Does combining ontology-based reasoning with a recommendation model improve recommendation relevance compared with suitable non-ontology baselines?

**Comparisons:** content-based, ontology-only, ML-only, and hybrid.

**Candidate measures:** NDCG@K and Precision@K as primary ranking measures; Recall@K and MAP@K where labels/query construction support them.

A fair comparison needs comparable candidate sets, queries, splits, tuning budgets, and metric definitions. Improvement is not presumed.

## RQ3 — Explanation usefulness
Do ontology-grounded explanations help users understand why an item or combination was recommended?

**Evidence:** structured participant evaluation after applicable ethics review.

**Candidate measures:** explanation clarity, usefulness, correctness, and confidence in understanding. Define scales and questionnaire wording before recruitment.

**Grounding:** every explanation claim should link to an identifiable user preference, item attribute, score component, or ontology path.

## RQ4 — Preference constraints and coverage
How do explicit user constraints and preferences affect relevance, diversity, and recommendation coverage across fashion and makeup?

**Comparisons:** ranking with/without preference features; hard constraints and soft preferences varied separately.

**Measures:** ranking relevance, intra-list diversity, catalogue coverage, hard-constraint violation rate.

## Provisional constructs
| Construct | Working definition | Candidate operationalisation |
|---|---|---|
| Relevance | Match to a labelled query or preference | Relevance labels or explicit feedback |
| Preference alignment | Agreement with explicit user preferences | Feature match or validated labels |
| Ontology compatibility | Match supported by defined ontology relations/rules | Query/rule-derived match feature |
| Explanation grounding | Traceability of explanation to evidence | Evidence ID, ontology path, score term |
| Diversity | Difference among items in a list | Defined attribute/embedding distance |
| Coverage | Portion of eligible catalogue that can be recommended | Unique recommended catalogue fraction |
| Constraint violation | Recommendation contradicting a hard constraint | Violations / eligible recommendations |

Finalise definitions before evaluation. Subjective constructs need annotation or questionnaire protocols.

## Proposed hypotheses
- H1: Hybrid ranking improves ranking quality over selected non-ontology baselines.
- H2: Ontology-grounded explanations improve user-rated clarity/usefulness over a comparator condition.
- H3: Explicit constraints improve preference-aligned relevance; diversity and coverage effects are measured separately.

## Decision log
| Decision | Status | Rationale / next action |
|---|---|---|
| Fashion and makeup in initial scope | Decided | User-selected scope |
| Face-image analysis in initial baseline | Excluded | Optional later work; privacy and validation concerns |
| Ranking metrics | Proposed | Confirm after data/labels selected |
| Human study | Conditional | Requires protocol and applicable ethics approval |
