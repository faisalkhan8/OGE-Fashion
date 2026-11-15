# Research Protocol
**Project:** OGE-Fashion  
**Protocol version:** 0.1 (initial proposal)  
**Status:** Draft for review; not preregistered  
**Date:** 2026-11-15

## 1. Working title
An Ontology-Guided Explainable Recommendation Framework for Personalised Fashion and Beauty Recommendations.

## 2. Background and motivation
Fashion and beauty recommendation involves interacting attributes: category, colour, style, occasion, material or finish, budget, and individual preferences. Recommendation models can rank items using observed features or learned representations. An ontology can represent explicit concepts and relationships and support semantic consistency and traceable reasoning.

This study will investigate whether and how a structured ontology can contribute to a hybrid recommendation pipeline for fashion and makeup. The combination itself is not asserted to be novel. Novelty must be established through a systematic literature review and a clearly delimited contribution.

## 3. Aim
Design and evaluate an ontology-guided recommendation framework for fashion and makeup that produces explanations grounded in user preferences, item attributes, ontology relationships, and model scores.

## 4. Objectives
1. Review fashion, beauty, explainable recommender, knowledge-graph, and ontology-based recommendation literature.
2. Identify lawful, documented data sources for clothing and makeup attributes.
3. Define a shared ontology with separate fashion and makeup subdomains.
4. Implement reproducible non-ontology baselines and an ontology-only matcher.
5. Implement a hybrid ranking method with interpretable score components.
6. Evaluate ranking quality, coverage, diversity, latency, and explanation usefulness.
7. Build a demonstrator after the research pipeline and data rights are sufficiently understood.

## 5. Research questions
- **RQ1:** How can a shared ontology represent fashion, makeup, user preferences, attributes, and compatibility relationships in a machine-readable way?
- **RQ2:** Does combining ontology-based reasoning with a recommendation model improve recommendation relevance compared with suitable non-ontology baselines?
- **RQ3:** Do ontology-grounded explanations help users understand why an item or combination was recommended?
- **RQ4:** How do explicit user constraints and preferences affect relevance, diversity, and recommendation coverage across fashion and makeup?

## 6. Hypotheses (to be tested)
- **H1:** A hybrid ontology-guided model will produce higher ranking quality than selected non-ontology baselines on the same eligible evaluation data.
- **H2:** Explanations grounded in ontology paths and score components will receive higher user-rated clarity/usefulness than explanations without explicit evidence paths.
- **H3:** Explicitly applying user constraints will improve preference-aligned relevance; effects on diversity and coverage will be measured rather than assumed.

Null results are valid. Refine hypotheses after literature review and data feasibility assessment, before test-set evaluation.

## 7. Scope and boundaries
### Included
- Fashion items and outfit components.
- Makeup categories: face, eye, and lip products/looks.
- Shared attributes: colour, style, occasion, budget, and preference.
- User-provided constraints and optional user-confirmed attributes.
- Item ranking and evidence-grounded explanation.

### Excluded initially
- Medical, dermatological, or skin-diagnosis advice.
- Claims that a face shape objectively determines suitable garments or makeup.
- Attractiveness scoring, identity recognition, ethnicity inference, age estimation, or other sensitive face analysis.
- Unconsented scraping of personal images or social profiles.
- Production commerce integrations before asset rights are confirmed.

Face-image analysis is optional later work, not a requirement for the initial recommender.

## 8. Conceptual framework
The system will combine:
1. **Catalogue representation:** items and documented attributes.
2. **User preference representation:** explicit preferences, exclusions, context, and constraints.
3. **Ontology reasoning:** semantic relationships, taxonomy, compatibility rules, and traceable paths.
4. **Recommendation models:** content-based and/or learned item scoring.
5. **Hybrid ranker:** combines calibrated model signals and ontology-derived features.
6. **Explanation layer:** reports only evidence traceable to data, scores, or ontology relationships.

A conceptual scoring template is:
`score(u,i,c) = w_m M(u,i,c) + w_o O(u,i,c) + w_p P(u,i,c) + w_c C(u,i,c)`
where M is the machine-learning/content signal, O is ontology compatibility, P is preference alignment, and C is context/constraint fit. This is a design template, not a committed final model. Tune weights on validation data; revise after literature review if needed.

## 9. Study design
A comparative offline evaluation will be conducted first, using the same eligible catalogue, user/query cases, candidate-generation policy, and data split across variants where methodologically appropriate.

Planned comparison arms:
- **B1 — Content-based:** item/user feature similarity without ontology reasoning.
- **B2 — Ontology-only:** semantic rules and ontology query results without a learned ranker.
- **B3 — ML-only:** machine-learning or embedding-based ranker without ontology compatibility features.
- **B4 — Hybrid:** combines selected model signals and ontology-derived features.

Potential ablations: hybrid without ontology features, without preference constraints, or without explanation output. Finalise these before test evaluation.

## 10. Data sources and governance
Candidate data sources are listed in [dataset-register.md](dataset-register.md). Initial candidates:
- Fashionpedia for clothing objects and attributes.
- DeepFashion for clothing attributes/retrieval, subject to its stated non-commercial research terms.
- Makeup datasets or catalogue metadata only after confirming provenance, labels, access conditions, and licence.
- A curated catalogue may be considered if annotation protocol and rights are documented.

A publicly downloadable dataset is not automatically approved for every use. Record owner/source, version/date, licence, permitted purposes, redistribution limits, attribution, consent/provenance, fields, and known bias. Keep restricted assets outside the public repository.

## 11. Annotation and preparation
For manually curated or annotated records:
- Write an annotation handbook with operational definitions and examples.
- Separate item attributes from subjective compatibility judgements.
- Use multiple annotators for subjective labels where feasible.
- Report suitable inter-rater agreement and adjudication.
- Keep provenance and licence metadata per source/item.
- Record missingness; do not silently treat missing as negative.

## 12. Evaluation plan
### Offline ranking
- Precision@K and Recall@K.
- NDCG@K.
- MAP@K where relevance labels and query structure support it.

### System-level
- Catalogue coverage.
- Intra-list diversity using a defined feature/embedding distance.
- Latency with runtime/hardware context and percentiles.
- Hard-constraint violation rate.

### Explanation/user evaluation
A separate study may assess perceived relevance, explanation clarity/usefulness, perceived control/trust, diversity, and personalisation. Define questionnaire and task protocol before recruitment. Determine sample-size rationale. Obtain required ethics review/approval, informed consent, data minimisation, and withdrawal/deletion procedures before recruiting or collecting participant data.

### Statistical analysis
- Freeze test set and evaluation code before final comparison.
- Tune hyperparameters and thresholds on training/validation only.
- Use paired comparisons when cases are shared.
- Report confidence intervals and effect sizes, not only p-values.
- Select statistical tests for the design and metric distributions.
- Address multiple comparisons where appropriate.
- Report null/negative results and uncertainty.

## 13. Bias, fairness, and safety
Risks include uneven catalogue representation, culturally narrow style taxonomies, demographic imbalance, lighting/colour variation, and assumed preferences. Mitigations:
- Do not claim universal cultural or aesthetic compatibility.
- Let users edit preferences and choose no preference.
- Allow exclusions and "do not recommend" options.
- Audit coverage and error patterns across documented catalogue groups.
- Avoid sensitive-attribute inference.
- State where evidence is insufficient.
- Distinguish data-derived associations from normative advice.

## 14. Reproducibility
Record source versions and checksums where permitted; processing scripts and seeds; split logic; model/config versions; ontology and reasoner versions; metric definitions; runtime environment; exclusions; failed runs; and protocol deviations. Never commit credentials or restricted data.

## 15. Limitations
Likely limitations include incomplete makeup data, noisy item metadata, limited preference labels, subjective compatibility, dataset/domain/cultural bias, and the gap between offline metrics and real-world user benefit. Offline ranking metrics alone do not establish practical benefit.

## 16. Indicative sequence and stage gates
This is a planning estimate, not a delivery commitment.

| Stage | Work | Exit evidence |
|---|---|---|
| S1 | Protocol, literature map, data due diligence, ontology spec | Reviewed documents and open-decision register |
| S2 | Ontology v0.1 and competency tests | Valid OWL artefact; recorded query/reasoner results |
| S3 | Dataset selection/preparation | Licence decision, data dictionary, reproducible preparation |
| S4 | Baselines | Reproducible baseline results on development data |
| S5 | Hybrid and ablations | Versioned model/config and validation results |
| S6 | Evaluation | Frozen test evaluation, uncertainty, limitations |
| S7 | Demonstrator | Cloud prototype using permitted/synthetic data |
| S8 | Paper | Complete manuscript with traceable evidence |

## 17. Protocol amendments
Changes to questions, hypotheses, inclusion criteria, data sources, splits, metrics, or analysis after test inspection must be documented with date, rationale, and impact. Do not silently rewrite the protocol to fit outcomes.

## 18. Starting references and resources
- Fashionpedia: https://fashionpedia.github.io/home/index.html
- DeepFashion: https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html
- W3C OWL 2 Overview: https://www.w3.org/TR/owl2-overview/
- W3C OWL 2 Primer: https://www.w3.org/TR/owl2-primer/
- Protégé: https://protege.stanford.edu/
- Optional future face-landmark exploration: https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker

These are starting resources, not a completed systematic review. Check bibliographic accuracy, relevance, and publication status before citing any paper.
