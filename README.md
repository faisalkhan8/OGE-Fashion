# OGE-Fashion

**An Ontology-Guided Explainable Recommendation Framework for Personalised Fashion and Beauty Recommendations**

OGE-Fashion investigates whether a provenance-aware semantic model can improve recommendation constraint satisfaction and make recommendation explanations more traceable across fashion and beauty domains.

> **Evidence status:** the ontology and validation suite are implemented; a deterministic synthetic benchmark is included. The benchmark is a software-method demonstration only, not evidence of real-user preference or population-level recommendation quality.

## Research question and problem statement

**Research question:** Does a provenance-aware OWL ontology with SHACL data constraints and SPARQL-executable competency rules improve hard-constraint satisfaction and explanation-trace coverage compared with a non-ontology colour/attribute-matching baseline, when both conditions use the same profiles, catalogue and held-out test split?

Recommendation systems can rank attribute-similar items while violating explicit occasion, dress-code or style constraints. OGE-Fashion models preferences, context, item attributes, compatibility assessments, recommendation results, explanations and evidence separately so that constraints and explanation provenance can be inspected.

The current benchmark operationalises a narrow subset of these ideas. It does not establish generalisation to real users.

## Provenance and project timeline

| Period | Work | Provenance boundary |
|---|---|---|
| **November 2023 – May 2024** | Historical BS Software Engineering Final Year Project (7th and 8th semesters), University of Sargodha. The original project explored ontology-supported clothing and makeup recommendations, including face-shape-related concepts. | Historical academic project. Exact original implementation details and outcomes require the original report, source artefacts or supervisor records. |
| **2026 research extension** | OGE-Fashion framework: OWL/Turtle model, Fashionpedia source-aligned taxonomy mapping, SHACL shapes, SPARQL competency queries, HermiT consistency checks, dataset due diligence and a reproducible synthetic recommender benchmark. | Later research and implementation. These activities are not backdated to the BS capstone period. |

See [historical FYP provenance](research/fyp-timeline.md).

## Architecture

- **Domain model:** OWL/Turtle classes and properties for fashion/makeup items, attributes, profiles, preferences, contexts, compatibility assessments, recommendations, explanations and evidence.
- **Source alignment:** Fashionpedia category and attribute records preserve source identifiers, labels, taxonomy levels and provenance. Lexical similarity is not asserted as semantic equivalence; unsupported owl:sameAs and owl:equivalentClass mappings are avoided.
- **Data constraints:** SHACL shapes validate synthetic profile, preference, budget, compatibility, recommendation, explanation and provenance records.
- **Query layer:** SPARQL competency questions test retrieval over the ontology and a synthetic fixture.
- **Reasoning:** HermiT is used for ontology consistency checks.
- **Benchmark:** a non-ontology baseline and an ontology-guided SPARQL-filtered condition are compared on the same deterministic synthetic test profiles.

## Verified implementation status

The merged ontology branch's latest successful CI runs reported:

| Check | Result | What it verifies |
|---|---:|---|
| RDF/Turtle structural validation | 3,237 triples parsed | Ontology parses and expected Fashionpedia records/provenance are present |
| HermiT reasoning | Consistent; 59 OWL classes loaded | No inconsistency or named class equivalent to owl:Nothing was reported |
| SPARQL competency queries | 12/12 passed | Query behaviour on the committed synthetic fixture |
| SHACL validation | 4/4 positive/negative tests passed | Synthetic records conform and selected invalid records are rejected |
| Foundation shade unit tests | 15/15 passed | Colour conversion, source parsing and shade-ranking implementation |

These are software/model validation results, not recommendation-performance results. See [ontology workflow](.github/workflows/ontology-validation.yml) and [shade workflow](.github/workflows/shade-baseline.yml).

### Foundation shade baseline

The repository also contains an attribute-retrieval baseline that ranks historical foundation swatches by CIEDE2000 colour difference. It compares displayed swatch colours only. It does **not** estimate skin tone, predict foundation suitability or infer user preference. See [the method note](docs/foundation-shade-baseline.md).

## Synthetic recommender benchmark

Install and run:

~~~bash
python -m pip install -r requirements-research.txt
python experiments/evaluate_recommender.py
python experiments/evaluate_recommender.py --demo
~~~

The experiment generates 24 synthetic profiles and evaluates both conditions on the same deterministic held-out split (seed 20261117). It writes results/metrics.json and results/evaluation_summary.md. The relevance labels are generated from the same constructed profile fields used by the constraints. Results therefore demonstrate behaviour on this fixture only; they are not independent evidence of user benefit.

## Reproducibility / quickstart

Python 3.12 is used in CI. From the repository root:

~~~bash
python -m pip install -r requirements-research.txt

# Parse ontology and verify source taxonomy/provenance
python scripts/validate_ontology.py

# OWL consistency and unsatisfiable-class checks (Java 17 required)
python scripts/reason_ontology.py

# 12 synthetic SPARQL competency tests
python scripts/test_competency_queries.py

# SHACL conformance and positive/negative tests
python scripts/validate_shacl.py
python scripts/test_shacl.py

# Standard-library foundation shade unit tests
python -m unittest discover -s tests -v

# Synthetic recommender benchmark and explanation trace
python experiments/evaluate_recommender.py
python experiments/evaluate_recommender.py --demo
~~~

The foundation shade sample command fetches its pinned upstream CSV and requires network access:

~~~bash
python -m oge_fashion.shade_baseline --target-hex F3CFB3 --top-k 5
~~~

## Current limitations and future work

- The recommender experiment uses **constructed synthetic profiles and catalogue records**. It does not use real users, observed preferences or an externally labelled benchmark.
- The benchmark uses encoded-sRGB Euclidean colour distance as a simple ranking signal; it is not a validated skin-tone or foundation-matching method.
- The current SPARQL benchmark operationalises a small set of constraints aligned with OGE properties. It does not invoke HermiT for per-request inference.
- Fashion/makeup vocabulary alignment remains preliminary and requires further relation-level review and expert assessment.
- Facial-image computer-vision classification is **future work**, not a demonstrated capability.
- Human user studies and explanation usefulness evaluation are **future work** and require appropriate ethics/consent review.
- A learned recommender, matched real-data experiments, statistical uncertainty analysis, deployed demonstrator and peer-reviewed publication are **future work**.
- Dataset rights differ across annotations, metadata, images and derived data. See the [dataset register](research/dataset-register.md).

## Repository map

- ontology/ — OWL/Turtle model, competency queries, SHACL shapes and source mappings.
- research/ — questions, protocol, literature evidence matrix, dataset due diligence and historical provenance.
- experiments/ — deterministic synthetic recommender benchmark.
- results/ — generated benchmark metrics and interpretation.
- oge_fashion/ — colour conversion, pinned shade-source loader and shade-ranking CLI.
- scripts/ — ontology, HermiT, SPARQL and SHACL validation utilities.
- tests/ — unit tests and synthetic RDF fixture.
- docs/ — method notes, workflow guidance and research summary.

## Research integrity

OGE-Fashion distinguishes source-derived facts, project modelling choices, synthetic test fixtures and empirical findings. Synthetic tests are never presented as user evidence. Historical FYP work is never conflated with the 2026 extension. Negative/null findings and limitations should be retained in future reporting.

## Licence

No repository-wide software licence has been selected. Until one is added, standard copyright applies to original repository code and documentation. Third-party dataset, annotation, image and metadata terms remain separate; consult the source-specific register before reuse.
