# Implementation Roadmap
**Planning baseline:** 16-week indicative sequence; estimates only, not commitments.

## Stage 1 — Research foundation
**Work:** review fashion/beauty recommenders, explainability, ontology/knowledge-graph recommendation; build a source matrix; confirm data licences; record protocol amendments.

**Exit evidence:** reviewed protocol, literature matrix, documented dataset decisions and unresolved items.

## Stage 2 — Ontology prototype
**Work:** convert specification to OWL 2; add synthetic individuals; implement competency queries; run syntax and reasoner validation.

**Exit evidence:** versioned OWL file, reproducible query tests, consistency/limitations report.

## Stage 3 — Data preparation
**Work:** select approved sources; map labels to ontology vocabulary; define inclusion/exclusion and deduplication; create leakage-aware data splits.

**Exit evidence:** reproducible scripts, provenance/licence manifest, auditable split generation.

## Stage 4 — Baselines
**Work:** implement content-based baseline, ontology-only matcher, and ML-only baseline if labels/data support it; define candidate generation and relevance labels.

**Exit evidence:** reproducible baselines and fixed metric definitions.

## Stage 5 — Hybrid and ablations
**Work:** combine ontology features with model outputs; implement configurable scoring; tune on validation only; run ablations.

**Exit evidence:** experiment configs, versioned model, validation results, no test tuning.

## Stage 6 — Evaluation
**Work:** freeze model/config; evaluate ranking, coverage, diversity, constraint violations, latency; quantify uncertainty; design user study and obtain approvals before recruitment.

**Exit evidence:** reproducible report including null findings, limitations, and relevant ethics documentation.

## Stage 7 — Demonstrator
**Work:** cloud-hosted prototype using permitted catalogue or synthetic records; expose preferences/exclusions; display evidence; implement privacy controls before collecting real user data.

**Exit evidence:** working demo, architecture notes, verified rights, no restricted research data exposed.

## Stage 8 — Paper
**Work:** write with actual methods/results; verify venue scope, fees, deadlines, review model and indexing; publish code/data only where permitted.

**Exit evidence:** complete manuscript and reproducibility package; no claim of acceptance before formal acceptance.

## Sprint 1 tasks
1. Confirm repository settings and description.
2. Review protocol and questions.
3. Create literature evidence matrix.
4. Complete Fashionpedia/DeepFashion licence review.
5. Investigate makeup data candidates.
6. Convert ontology proposal to OWL 2 draft.
7. Add synthetic examples and competency-query tests.
8. Verify cloud workflow without large local downloads.
