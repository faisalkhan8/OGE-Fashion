# OGE-Fashion
**An Ontology-Guided Explainable Recommendation Framework for Personalised Fashion and Beauty Recommendations**

OGE-Fashion investigates how a shared fashion-and-beauty ontology can be combined with machine-learning recommendation methods to generate personalised recommendations with traceable explanations.

> **Research status:** proposal and design stage. No performance results, user-study findings, or validated recommendation claims are reported.

## Scope
- **Fashion:** garments, outfits, categories, colours, patterns, materials, fit, and style.
- **Makeup:** face, eye, and lip makeup categories; colours; finishes; application styles; product attributes.
- **Shared concepts:** user preferences, constraints, budgets, occasions, styles, colours, and compatibility relationships.

Facial-image analysis is optional future work, not a dependency for the first experiments. Explicit user-entered or user-confirmed attributes are preferred.

## Research positioning
Prior work already includes OWL-based personalised fashion recommendation, explainable fashion compatibility, makeup recommendation, cosmetic-product recommenders dating back to 2004, and separate systems for occasion-based clothing and facial makeup advice. OGE-Fashion therefore does not claim to invent ontology-guided fashion or makeup recommendation. Its tentative direction is to evaluate alignment of existing fashion vocabularies with makeup concepts and shared user/context preferences, then test evidence-grounded explanations. See the [literature evidence matrix](research/literature/evidence-matrix.md); novelty is not yet established.

## Research questions
1. How can a shared ontology represent fashion, makeup, user preferences, attributes, and compatibility relationships in a machine-readable way?
2. Does combining ontology-based reasoning with a recommendation model improve recommendation relevance compared with suitable non-ontology baselines?
3. Do ontology-grounded explanations help users understand why an item or combination was recommended?
4. How do explicit user constraints and preferences affect relevance, diversity, and recommendation coverage across fashion and makeup?

These are research questions, not established findings. See [research protocol](research/research-protocol.md).

## Planned comparison
1. Content-based recommendation baseline.
2. Ontology-only semantic matching.
3. Machine-learning recommendation without ontology reasoning.
4. Hybrid ranking combining learned signals and ontology-based compatibility.

Candidate ranking metrics include Precision@K, Recall@K, NDCG@K, and MAP@K. Coverage and diversity will also be measured. Explanation usefulness requires separate human evaluation. Data rights, split strategy, and ethics requirements must be addressed before experiments.

## Repository structure
- `research/literature/`: preliminary literature evidence matrix and review-search method.
- `research/`: protocol, questions, dataset register.
- `ontology/`: ontology specification and competency questions.
- `docs/`: roadmap and cloud-first workflow.

## Cloud-first development
Use GitHub as the source of truth and a browser-based environment such as GitHub Codespaces or a hosted notebook for implementation. Do not download large datasets to the laptop. Keep raw/restricted assets and model checkpoints outside Git; commit only permitted code, documentation, manifests, and small synthetic fixtures. Check cloud quotas and billing before starting compute.

## Integrity, licensing, and responsible use
- Confirm dataset and asset rights before downloading, redistributing, or using assets in a deployed product.
- Do not infer sensitive traits or make attractiveness judgements.
- Do not collect face images by default. Any future face-image feature must be optional, consent-based, minimised, and user-correctable.
- Follow applicable institutional ethics review and consent requirements before human-participant recruitment.
- Tune on training/validation data only; preserve an untouched test set.
- Report negative and null results, limitations, and methodology.

## Current status
**Sprint 1:** research protocol, questions, dataset due diligence, ontology specification, and cloud workflow setup. No deployed product, evaluated model, publication, or empirical finding is claimed.

## Contribution
Use GitHub Issues for research decisions and implementation tasks. Ontology changes should state the competency question, class/property change, expected reasoning behaviour, evidence/rationale, and compatibility impact.

## Licence
No software licence has been selected yet. Until a licence is added, standard copyright applies; public visibility does not automatically grant reuse rights. Dataset and third-party asset licences are separate.
