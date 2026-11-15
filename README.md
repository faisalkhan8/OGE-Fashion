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
- `research/makeup-data-review.md`: makeup dataset candidates, rights, limitations, and initial data plan.
- `research/data-profiling.md`: source-level profile results and data-quality observations.
- `research/`: protocol, questions, dataset register, data profiling, and a historical FYP timeline that separates the 2023–2024 degree project from the later research extension.
- `ontology/`: ontology specification, competency questions, preliminary vocabulary alignment, Fashionpedia source mappings (46 categories and 294 attributes), SPARQL query templates, and the OWL 2/Turtle structural draft.
- `docs/`: roadmap, cloud-first workflow, and foundation shade baseline.
- `oge_fashion/`: colour conversion, pinned shade-source loader, and ranking CLI.
- `tests/`: standard-library unit tests and synthetic RDF/SPARQL fixture data.
- `scripts/`: metadata-only external catalogue profiling tools, RDF/source-integrity validation, and the dedicated SPARQL competency-query test runner.

## Cloud-first development
Use GitHub as the source of truth and a browser-based environment such as GitHub Codespaces or a hosted notebook for implementation. Do not download large datasets to the laptop. Keep raw/restricted assets and model checkpoints outside Git; commit only permitted code, documentation, manifests, and small synthetic fixtures. Check cloud quotas and billing before starting compute.

## Integrity, licensing, and responsible use
- Confirm dataset and asset rights before downloading, redistributing, or using assets in a deployed product.
- Do not infer sensitive traits or make attractiveness judgements.
- Do not collect face images by default. Any future face-image feature must be optional, consent-based, minimised, and user-correctable.
- Follow applicable institutional ethics review and consent requirements before human-participant recruitment.
- Tune on training/validation data only; preserve an untouched test set.
- Report negative and null results, limitations, and methodology.

## Initial implementation
The first foundation-shade attribute baseline is implemented under `oge_fashion/`, with unit tests in `tests/` and a GitHub Actions workflow. It fetches a pinned shade CSV at runtime, converts sRGB HEX values to CIELAB, and ranks swatches using CIEDE2000. See [foundation shade baseline](docs/foundation-shade-baseline.md) and [data profiling](research/data-profiling.md). The metadata-only Open Beauty Facts profiler is in scripts/profile_open_beauty_facts.py, with a rate-limited GitHub Actions workflow. Its first profile returned 968 API matches for the makeup tag; the first 100 records had 84% ingredient-text coverage and 0% allergen-tag coverage. The profile is suitable only for metadata prototyping, not allergen or safety decisions. The hosted CI run passed 15 unit tests and the sample ranking.

The baseline compares displayed product swatches only. It does not predict skin tone, foundation suitability, or personal preference.

## Current status
**Sprint 1 (research extension, 2026-11-15):** research protocol, questions, initial dataset due diligence and metadata profiling, concept-level prior-art alignment, and an OWL 2/Turtle structural draft. The ontology draft now represents the 46 extracted Fashionpedia category entries and 294 attribute entries as provenance-bearing named individuals. Twelve SPARQL competency-query templates, a synthetic fixture, a Python test runner, and a GitHub Actions workflow have been added. The latest GitHub Actions run parsed 3,237 RDF triples; verified the 46 category and 294 attribute source entries and their provenance; ran Owlready2 0.51 with HermiT over 59 OWL classes with no ontology inconsistency or named unsatisfiable classes; and passed all 12 synthetic SPARQL tests. The independent foundation shade workflow also passed all 15 tests and its sample ranking. RDF parsing, structural checks, HermiT consistency, and synthetic query behaviour are validated; source semantics and recommendation quality are not. Further source-relation review, makeup vocabulary alignment, evaluation protocol and labels, model comparisons, user evaluation, deployment, and publication remain outstanding. The original university FYP period is recorded separately as semesters 7 and 8 (November 2023–May 2024). No deployed product, evaluated model, publication, or empirical recommendation-quality finding is claimed.

## Contribution
Use GitHub Issues for research decisions and implementation tasks. Ontology changes should state the competency question, class/property change, expected reasoning behaviour, evidence/rationale, and compatibility impact.

## Licence
No software licence has been selected yet. Until a licence is added, standard copyright applies; public visibility does not automatically grant reuse rights. Dataset and third-party asset licences are separate.
