# PhD Research Extension: Provenance-Aware Evidence Quality in Explainable Recommendation

**Status:** Research direction proposal — not yet implemented or empirically validated  
**Prepared:** 2026-11-22  
**Working branch:** `phd-prep/caverlee-knowledge-grounded-recsys`

## 1. Purpose

This document proposes a PhD-focused extension of OGE-Fashion. It preserves the existing ontology and provenance work while examining evidence quality, provenance, conflict handling and abstention in recommendation explanations. A focused literature screen shows that LLM + KG explainable recommendation, graph-retrieved evidence and factuality evaluation are already established areas; the intended contribution is therefore not simply to add an LLM to a knowledge graph. See the [focused literature evidence matrix](literature/explainable-recommender-evidence-matrix.md).

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

**Provenance-Aware Evidence Quality and Abstention in Explainable Recommendation**

Fashion and beauty are the initial application domain inherited from OGE-Fashion. The research contribution should be framed around generalisable recommendation and explanation methods, with fashion as a testbed only where the data supports that scope.

## 4. Proposed problem

A recommender can produce a plausible-sounding explanation that overstates what its evidence establishes. Prior work already combines LLMs with collaborative signals, knowledge graphs, retrieved graph paths and subgraph reasoning for explainable recommendations (including G-Refer, K-RagRec and KAPER). Separate work has evaluated claim-level factual consistency. Therefore, simply providing graph evidence to an LLM or measuring factuality is not a novel claim.

The narrower question is how recommendation explanations should preserve and communicate the source, version, time, evidence status and reliability of the records they use—especially when attributes are missing, stale, conflicting, or inferred. The project will test whether a provenance-aware verification and abstention layer adds measurable value beyond existing graph-grounded explanation approaches.

The proposed system will investigate how to combine:
1. observed user-item interactions, separately labelled user-confirmed preferences, and model-inferred profile attributes;
2. product catalogue facts linked to source identifiers, source versions, timestamps and provenance;
3. a recommendation model or ranker and a reviewed ontology / knowledge graph;
4. an explanation generator conditioned on identifiable evidence records;
5. a verifier that checks evidence identity, status, conflict and temporal validity before permitting factual claims or abstaining.

The explanation generator must not invent item attributes, preferences, or ontology relations. When evidence is missing, it should state that the system cannot substantiate the claim.

## 5. Proposed research questions

- **RQ1 — Evidence provenance:** How can a recommendation pipeline represent the provenance, version, timestamp and epistemic status of interaction and catalogue evidence used in a user/item explanation?
- **RQ2 — Evidence quality:** Under missing, conflicting, stale and controlled-corruption conditions, how accurately can the system identify supported, contradicted, unsupported and unverified explanation claims?
- **RQ3 — Abstention and utility:** What trade-offs arise between recommendation ranking, claim support, appropriate abstention, coverage, diversity and latency when provenance-aware verification is applied?
- **RQ4 — User understanding:** Do users better understand the limits of recommendation evidence when explanations distinguish observed behaviour, user-confirmed preferences, catalogue facts and model inferences?

These questions are provisional. The focused literature matrix identifies close prior work, including KAPER (2026) and the PAKDD 2026 factual-consistency study. The research contribution and hypotheses must be revised after reading these papers and tracing their citations; no novelty claim is currently made.

## 6. Candidate hypotheses (to be reviewed before test evaluation)

- **H1:** Adding provenance and record-status checks will reduce the rate of unsupported or contradicted factual claims under controlled missing/conflicting-evidence tests, compared with an otherwise matched graph/LLM explanation baseline.
- **H2:** Explicit abstention when evidence is missing, stale or inconsistent will improve appropriate-abstention and claim-support rates, with measurable trade-offs in explanation coverage and latency.
- **H3:** Any ranking-quality or user-understanding benefit is an empirical question; no improvement is presumed.

These are candidate hypotheses only. The evaluation must distinguish controlled perturbations from naturally occurring catalog errors. Null or negative findings are valid. Hypotheses and analysis plans must be fixed before inspecting held-out test outcomes.

## 7. Proposed system and experiment arms

The following comparison is a design proposal, not an implemented feature set. It must include reproduction or adaptation of at least one close graph-grounded prior method, subject to code, data and licence availability:

| Arm | Recommendation | Explanation |
|---|---|---|
| B1 — Non-ontology baseline | Reproducible content-based or interaction-based ranker | No generated evidence explanation |
| B2 — Structured-knowledge baseline | Ontology/knowledge-graph constraints and features | Structured trace or template |
| B3 — LLM reasoning baseline | LLM-based personalisation/reasoning, following a carefully documented adaptation of ReasoningRec or LangPTune where feasible | LLM-generated natural-language explanation |
| B4 — Graph-grounded baseline | A reproducible adaptation of G-Refer, K-RagRec or KAPER, selected after code/data review | Retrieved graph paths or structured evidence rendered for the LLM |
| B5 — Provenance-aware candidate | Matched recommender and explanation generator with record-level provenance, version/status checks and conflict handling | Claim verification plus explicit abstention when evidence is not supportable |

Ablations should isolate the contribution of knowledge-graph evidence, hard constraints, and claim verification. Comparisons must use the same eligible data, user/query cases, candidate sets, splits, and tuning policy wherever methodologically appropriate.

ReasoningRec should be studied and, if feasible, reproduced or adapted as a baseline. Its reported results must not be copied into OGE-Fashion or treated as results of this project.

## 8. Evaluation plan

### Recommendation quality
- NDCG@K and Precision@K as candidate primary ranking measures.
- Recall@K or MAP@K where label structure supports them.
- Hard-constraint violation rate.
- Catalogue coverage and intra-list diversity.
- Runtime/latency with hardware and software configuration recorded.

### Explanation quality and evidence status
- Claim-level support precision and recall against a reviewed reference set.
- Contradiction rate and unsupported-claim rate.
- Correct detection of missing, stale, conflicting, revoked or model-inferred records.
- Appropriate-abstention rate and over-abstention rate.
- Provenance trace completeness (source, record ID, version, timestamp and derivation).
- Counterfactual consistency under controlled changes to cited records.
- Human ratings of clarity and understanding of evidence limitations, only after appropriate ethics review and informed consent.

Automated language-model judging should not be treated as ground truth. Human assessment, rule-based evidence checks, and expert review should be reported separately.

### Statistical discipline
Use train/validation/test separation, freeze the evaluation code before final test runs, tune only on training/validation data, report uncertainty intervals and effect sizes, and retain failed or negative results. Avoid claims based only on a handful of synthetic examples.

## 9. Initial real-data candidate: H&M Personalized Fashion Recommendations

The first candidate for a non-commercial fashion recommendation evaluation is the H&M Personalized Fashion Recommendations dataset hosted on Kaggle. Its official data description specifies chronological customer purchase history, article metadata, customer metadata, and optional article images. The official competition rules permit non-commercial academic research but prohibit redistributing the competition data or sharing it with people who have not accepted the rules.

- Dataset: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data
- Competition rules: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/rules

The dataset is **not downloaded or accepted yet**. Use is conditional on the applicant personally registering and accepting the current rules. Keep raw data outside GitHub and CI. Phase one should process only the CSV files and exclude customer age/postal code and images unless a later, separately justified research question and rights review require them. The available records support temporal purchase interactions and product metadata, but the dataset does not by itself provide a history of catalogue revisions. Missing/conflicting attribute scenarios must therefore be explicitly labelled as controlled perturbation experiments, not as observed real-world catalogue drift.

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

## 15. Literature and novelty gate

Before finalising the research contribution, complete the paper-by-paper review in [the explainable recommender evidence matrix](literature/explainable-recommender-evidence-matrix.md). At minimum, read KAPER (2026), G-Refer (WWW 2025), K-RagRec (ACL 2025), Kabongo & Guigue (PAKDD 2026), ReasoningRec (NAACL 2025) and LangPTune (CIKM 2025) in full. Record methods, data, evaluation and exact differences. Until this review and citation-chaining are complete, use language such as 'candidate question' and 'we will investigate'; do not use 'novel', 'first', or 'state of the art'.

## 16. Integrity and authorship

This file describes a research plan, not research results. All future work must distinguish:
- implementation from empirical validation;
- synthetic test fixtures from real-world datasets;
- generated explanations from verified explanations;
- proposed hypotheses from supported findings;
- independent work from third-party methods and code.

Do not use automated paper-writing software to create claims, citations, data, or results that have not been independently checked. Any manuscript must be authored and verified by the named researchers, with methods, code, data rights, and limitations stated transparently.
