# PhD Research Extension: Evidence-Grounded Explainable Recommendation

**Status:** Research direction proposal — not yet implemented or empirically validated  
**Prepared:** 2026-11-22  
**Working branch:** `phd-prep/caverlee-knowledge-grounded-recsys`

## 1. Purpose

This document proposes a PhD-focused extension of OGE-Fashion. It preserves the existing ontology and provenance work while connecting it to research on LLM-based recommendation and human-interpretable explanations.

The project is **not** being presented as a completed paper, a validated real-world recommender, or a reproduction of another researcher's system. The proposed extension must first be checked against the literature, implemented, and evaluated.

## 2. Initial faculty-fit case: Professor James Caverlee

Professor James Caverlee (Computer Science and Engineering, Texas A&M University) lists recommender systems, large language models, data mining, trustworthy machine learning, and information retrieval among his research interests. His group describes work on trustworthy and efficient recommendation.

A particularly relevant paper is:

> Millennium Bismay, Xiangjue Dong, and James Caverlee. 2025. *ReasoningRec: Bridging Personalized Recommendations and Human-Interpretable Explanations through LLM Reasoning*. Findings of NAACL 2025, pp. 8147–8163. DOI: https://doi.org/10.18653/v1/2025.findings-naacl.454

ReasoningRec uses LLMs to represent user preferences and aversions, generates synthetic explanatory reasoning with a larger LLM, and uses this material to fine-tune a smaller model for recommendation and explanation. The paper reports the importance of contextual and personalised input for plausible explanations.

**Potential point of connection:** OGE-Fashion currently represents user preferences, item properties, constraints, ontology relations, and provenance explicitly. This creates a possible complementary research question: can recommendations and LLM-generated explanations be grounded in inspectable, structured evidence rather than relying only on generated natural-language reasoning?

This is a proposed research direction, not a claim that the gap is novel. A focused literature review must compare it with knowledge-aware, graph-grounded, faithful, and explainable recommender systems before any novelty claim is made.

Useful starting points:
- Professor profile and research: https://engineering.tamu.edu/cse/profiles/jcaverlee.html
- Professor's research website and publications: https://people.engr.tamu.edu/caverlee/
- Prospective PhD students guidance: https://people.engr.tamu.edu/caverlee/prospective.html
- ReasoningRec paper: https://aclanthology.org/2025.findings-naacl.454/
- ReasoningRec code: https://github.com/millenniumbismay/reasoningrec

## 3. Proposed working title

**Evidence-Grounded Reasoning for Faithful and Constraint-Aware Explainable Recommendations**

Fashion and beauty are the initial application domain inherited from OGE-Fashion. The research contribution should be framed around generalisable recommendation and explanation methods, with fashion as a testbed only where the data supports that scope.

## 4. Proposed problem

A recommender can produce a plausible-sounding explanation that is not fully supported by the user's stated preferences, the recommended item's actual attributes, or the system's constraint checks. LLM-based reasoning may improve the readability of explanations, while structured knowledge representations may provide inspectable evidence.

The proposed system will investigate how to combine:
1. explicit user preferences, dislikes, context, and hard constraints;
2. a provenance-aware ontology or knowledge graph;
3. a recommendation model or ranker;
4. an explanation generator that receives identifiable evidence;
5. a verification layer that checks explanation claims against the evidence.

The explanation generator must not invent item attributes, preferences, or ontology relations. When evidence is missing, it should state that the system cannot substantiate the claim.

## 5. Proposed research questions

- **RQ1 — Evidence grounding:** To what extent can structured ontology/knowledge-graph evidence ground LLM-generated recommendation explanations in explicit user preferences, item attributes, and context?
- **RQ2 — Faithfulness and constraint adherence:** Does evidence-grounded generation reduce unsupported explanation claims and hard-constraint violations compared with an LLM-only explanation condition?
- **RQ3 — Recommendation trade-offs:** What effects do evidence grounding and hard constraints have on ranking quality, catalogue coverage, diversity, and latency?
- **RQ4 — Human understanding:** Do users find evidence-grounded explanations clearer, more useful, and more trustworthy than matched explanations without explicit evidence traces?

These questions are provisional. Final wording and hypotheses depend on literature review, dataset feasibility, and the actual methods that can be implemented.

## 6. Candidate hypotheses (to be reviewed before test evaluation)

- **H1:** The evidence-grounded condition will produce fewer unsupported or contradicted explanation claims than an LLM-only explanation condition.
- **H2:** Explicit hard-constraint enforcement will reduce constraint violations, while its effects on ranking quality, diversity, and catalogue coverage will be measured rather than assumed.
- **H3:** Evidence-grounded explanations may improve user-rated clarity and usefulness, subject to a properly reviewed human evaluation.

Null or negative findings are valid. Hypotheses and analysis plans must be fixed before inspecting held-out test outcomes.

## 7. Proposed system and experiment arms

The following comparison is a design proposal, not an implemented feature set:

| Arm | Recommendation | Explanation |
|---|---|---|
| B1 — Non-ontology baseline | Reproducible content-based or interaction-based ranker | No generated evidence explanation |
| B2 — Structured-knowledge baseline | Ontology/knowledge-graph constraints and features | Structured trace or template |
| B3 — LLM reasoning baseline | LLM-based personalisation/reasoning, following a carefully documented adaptation of relevant prior work | LLM-generated natural-language explanation |
| B4 — Evidence-grounded hybrid | Matched recommendation model with structured evidence and explicit constraints | LLM explanation conditioned on evidence IDs/paths, followed by claim checking |

Ablations should isolate the contribution of knowledge-graph evidence, hard constraints, and claim verification. Comparisons must use the same eligible data, user/query cases, candidate sets, splits, and tuning policy wherever methodologically appropriate.

ReasoningRec should be studied and, if feasible, reproduced or adapted as a baseline. Its reported results must not be copied into OGE-Fashion or treated as results of this project.

## 8. Evaluation plan

### Recommendation quality
- NDCG@K and Precision@K as candidate primary ranking measures.
- Recall@K or MAP@K where label structure supports them.
- Hard-constraint violation rate.
- Catalogue coverage and intra-list diversity.
- Runtime/latency with hardware and software configuration recorded.

### Explanation quality and faithfulness
- Claim-level support rate: proportion of verifiable explanation claims linked to valid preference, item, context, or ontology evidence.
- Contradiction rate: proportion of claims that conflict with available records.
- Evidence trace completeness and validity.
- Counterfactual consistency: test whether an explanation changes appropriately when a relevant preference or item attribute is altered.
- Human ratings of clarity, usefulness, and perceived trust, only after appropriate ethics review and informed consent.

Automated language-model judging should not be treated as ground truth. Human assessment, rule-based evidence checks, and expert review should be reported separately.

### Statistical discipline
Use train/validation/test separation, freeze the evaluation code before final test runs, tune only on training/validation data, report uncertainty intervals and effect sizes, and retain failed or negative results. Avoid claims based only on a handful of synthetic examples.

## 9. Initial real-data candidate: H&M Personalized Fashion Recommendations

The first candidate for a non-commercial fashion recommendation evaluation is the H&M Personalized Fashion Recommendations dataset hosted on Kaggle. Its official data description specifies chronological customer purchase history, article metadata, customer metadata, and optional article images. The official competition rules permit non-commercial academic research but prohibit redistributing the competition data or sharing it with people who have not accepted the rules.

- Dataset: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data
- Competition rules: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/rules

The dataset is **not downloaded or accepted yet**. Use is conditional on the applicant personally registering and accepting the current rules. Keep raw data outside GitHub and CI. Phase one should process only the CSV files and exclude customer age/postal code and images unless a later, separately justified research question and rights review require them.

Purchases provide implicit behavioural evidence, not explicit statements of preference. A model may infer interests from purchase history, but explanations must not call inferred interests user-confirmed preferences. The seven-day next-purchase task in the original competition and MAP@12 provide a useful benchmark reference; the research protocol should define its own temporal train/validation/test split and must not access hidden competition test labels.

The full access, schema-mapping, privacy, split, metrics and publication gates are documented in [the H&M real-data evaluation plan](hm-real-data-evaluation-plan.md). This dataset can support a real-data ranking experiment, but it cannot by itself establish explanation usefulness, causal purchase impact, or makeup recommendation quality.

## 10. Data strategy and governance

The current OGE-Fashion recommender benchmark uses 24 constructed profiles, 6 held-out synthetic profiles, and 18 synthetic items. Its labels are derived from fields used by its constraints. It is a useful software-level demonstration, but it cannot establish real-user relevance, population-level recommendation quality, or explanation usefulness.

The research extension must therefore identify at least one legally usable dataset with suitable user-item interaction or preference evidence and documented item attributes. Candidate sources must be evaluated individually for:
- access conditions and licence;
- permitted research and redistribution uses;
- provenance, consent, and privacy conditions;
- completeness and reliability of item attributes;
- coverage and likely dataset bias;
- compatibility between interaction records and ontology concepts.

A downloadable dataset is not automatically licensed for every intended use. Do not commit restricted data, credentials, personal user records, or unlicensed images to this public repository.

If no suitable real interaction dataset can be used lawfully, the project must narrow its claims and describe the evaluation as a controlled benchmark rather than imply real-user validation.

## 11. Human-subject research and safety

No participant recruitment, user study, or collection of new personal data should begin until the applicable institution has determined whether ethics/IRB review or approval is required. The study should use informed consent, data minimisation, defined retention/deletion procedures, and voluntary withdrawal.

The initial scope excludes sensitive face analysis, identity recognition, ethnicity inference, attractiveness scoring, and medical or dermatological recommendations. User preferences must remain editable and must not be inferred from sensitive characteristics.

## 12. What already exists in OGE-Fashion

The current main branch documents:
- a provenance-aware OWL/Turtle model;
- Fashionpedia-aligned source taxonomy records;
- SHACL shapes and SPARQL competency queries;
- HermiT ontology consistency checks;
- a deterministic synthetic recommendation benchmark;
- a research protocol and dataset due-diligence records.

The recorded software checks include 3,237 parsed RDF triples, 59 OWL classes, 12/12 SPARQL competency checks, 4/4 SHACL tests, and 15/15 foundation-shade unit tests. These verify selected implementation properties and are not evidence of user benefit.

The current benchmark reports better metrics for the ontology-filtered synthetic condition, but the relevance labels are derived from the same constructed fields used by the constraints. The results therefore demonstrate behaviour on that fixture only. They must remain labelled synthetic in all CV, SOP, outreach, and research materials.

The 2023–2024 undergraduate FYP and the 2026 research extension must remain clearly separated in project history and attribution.

## 13. Implementation gates

1. **Literature gate:** read ReasoningRec in full; map relevant work on knowledge-aware recommendation, evidence-grounded LLM explanations, explanation faithfulness, constraint-aware recommendation, and fairness/trustworthiness.
2. **Data gate:** select a permitted real dataset or formally narrow the intended claims; publish a source and licence register.
3. **Specification gate:** revise the ontology and protocol only where the literature and competency questions justify it; version all amendments.
4. **Baseline gate:** implement and test matched non-ontology, knowledge-based, and LLM reasoning baselines.
5. **Hybrid gate:** implement evidence-conditioned explanation generation and claim verification; log model versions, prompts, seeds, and configurations.
6. **Evaluation gate:** run a frozen test evaluation with uncertainty and ablations; report negative findings.
7. **Human evaluation gate:** obtain applicable ethics determination/approval before participant work.
8. **Writing gate:** prepare a manuscript only from completed, reproducible methods and results, with every citation and claim manually verified.

## 14. Application positioning

For a Texas A&M CSE PhD application, the research statement should focus on a specific question and connect it to one or two relevant Caverlee-group papers. Professor Caverlee's published prospective-student guidance says PhD admissions are handled through the departmental process and that applicants should make their case in the application; it discourages generic emails asking for a chance assessment or materials review.

The project should be described accurately as an independent research extension in progress. Do not imply Professor Caverlee has endorsed, supervised, or collaborated on it.

Texas A&M CSE's published Fall PhD deadline is December 15. Its English-language requirements must be checked separately: a University of Sargodha Medium of Instruction letter should not be described as an automatic waiver unless the university confirms that in writing.

## 15. Integrity and authorship

This file describes a research plan, not research results. All future work must distinguish:
- implementation from empirical validation;
- synthetic test fixtures from real-world datasets;
- generated explanations from verified explanations;
- proposed hypotheses from supported findings;
- independent work from third-party methods and code.

Do not use automated paper-writing software to create claims, citations, data, or results that have not been independently checked. Any manuscript must be authored and verified by the named researchers, with methods, code, data rights, and limitations stated transparently.
