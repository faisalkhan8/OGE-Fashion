# Literature evidence matrix — explainable recommendation, LLMs, graphs and factuality

**Prepared:** 2026-11-22  
**Status:** focused scoping review; not a systematic literature review and not a novelty claim.

## Executive finding

The broad idea of combining large language models (LLMs), knowledge graphs (KGs), and recommendation explanations is already well represented in published work. In particular, ReasoningRec, XRec, G-Refer, K-RagRec, subgraph-reasoning methods, and KAPER address close variants of LLM-assisted explainable recommendation and graph-grounded explanations. Separate work has evaluated the factual consistency of text-based recommendation explanations. OGE-Fashion must not claim to introduce LLM + KG recommendation, graph-retrieved explanations, or explanation factuality evaluation in general.

A defensible direction to investigate is narrower: **how a recommendation system records, versions, checks, and communicates the provenance and reliability of the specific evidence used in a recommendation explanation when catalogue evidence is missing, stale, conflicting, or inferred**. This is a candidate research question only. The literature review must determine whether it is genuinely underexplored and whether an implementable, measurable contribution exists.

## Evidence matrix

| Work | Published venue / year | What it establishes | Implication for OGE-Fashion |
|---|---|---|---|
| Ma, Ren & Huang, **XRec: Large Language Models for Explainable Recommendation** | Findings of EMNLP 2024 | Model-agnostic use of LLMs for explanations using collaborative-filtering signals | Do not claim LLM-generated explanation for recommendation is new |
| Qin et al., **Beyond Persuasion: Towards Conversational Recommender System with Credible Explanations** | Findings of EMNLP 2024 | Credibility-aware generation and post-hoc refinement for conversational recommendations | Credibility and avoiding misleading explanations already have methods |
| Bismay, Dong & Caverlee, **ReasoningRec: Bridging Personalized Recommendations and Human-Interpretable Explanations through LLM Reasoning** | Findings of NAACL 2025 | LLM-generated preference/aversion representations and synthetic explanation reasoning used to fine-tune a smaller LLM | Direct faculty-fit paper for Professor Caverlee; study the actual method and datasets before proposing an extension |
| Li et al., **G-Refer: Graph Retrieval-Augmented Large Language Model for Explainable Recommendation** | The Web Conference (WWW) 2025 | Retrieves structural and semantic collaborative-filtering signals from graphs, translates them into text, and uses them in LLM explanations | Graph retrieval + LLM explanation is established prior art |
| Wang et al., **Knowledge Graph Retrieval-Augmented Generation for LLM-based Recommendation (K-RagRec)** | ACL 2025 | Retrieves structured KG information to augment LLM-based recommendation and address noise/structure limitations of vanilla RAG | KG-RAG recommendation already exists; do not present graph retrieval as novelty |
| Shi et al., **LLM-powered explanations: Unraveling recommendations through subgraph reasoning** | Knowledge-Based Systems, 4 Nov 2025 | Uses LLMs to enrich KGs from review-derived triples, subgraph reasoning and generated explanations; evaluates on four real-world datasets and a company application | Subgraph reasoning and LLM explanation generation are already combined |
| Gao et al., **LangPTune: Optimizing Language-based User Profiles for Recommendation** | CIKM 2025 | End-to-end training of natural-language user profiles against recommendation objectives, with interpretability evaluation | Relevant Cornell/Professor Joachims fit; distinguish explicit provenance/record-level evidence from readable but generated profiles |
| Polleti, de Souza & Cozman, **Generating explanations for knowledge-aware conversational recommendation systems** | User Modeling and User-Adapted Interaction, 20 Jun 2025 | Uses auxiliary KG and embeddings to generate balanced reasons for and against conversational recommendations; includes functional and human evaluations | Knowledge-aware explanation and balanced pro/con reasoning are prior art |
| Kabongo & Guigue, **On the Factual Consistency of Text-based Explainable Recommendation Models** | PAKDD 2026 | Builds statement-level factual ground truth from reviews and proposes LLM/NLI-based alignment metrics; evaluates six explainable recommendation models | Claim-level factuality metrics exist; OGE must build on and compare with this work, not claim to introduce factuality evaluation |
| Kim, Kim & Kim, **Leveraging graph path evidence for explainable recommender systems (KAPER)** | Knowledge-Based Systems, 19 Jul 2026 | Computes user-attribute preferences using recency, frequency, deviation and TF-IDF; selects graph-path evidence with temporal/structural weighting; conditions LLM reranking and explanation generation | Very recent and close to evidence-grounded graph recommendation; read full text and compare before deciding if the proposed gap survives |
| Kabongo, Satouf & Guigue, **Rank, Don't Generate: Statement-level Ranking for Explainable Recommendation** | ICTIR 2026 | Uses statement-level ranking for explainable recommendation | Read for alternatives to free-form LLM explanation generation and how explanation selection is evaluated |

## Proposed narrower question to investigate

**How can a recommender preserve and validate the source, version, timestamp, and status of each item/user evidence record used in an explanation, and how should it respond when evidence is missing, stale, inferred, or contradictory?**

Possible evaluation conditions, subject to literature refinement:
1. Standard interaction/content recommendation with no explanation.
2. LLM explanation from a user/item text profile.
3. Graph/KG evidence-conditioned explanation reproducing or adapting a suitable prior method (for example G-Refer or KAPER, subject to code/data access and reproducibility).
4. Provenance-aware condition that carries evidence identifiers and source metadata into the explanation pipeline and performs record/schema checks before exposing factual claims.

Potential interventions:
- remove selected product attributes;
- introduce controlled conflicting values with explicit record provenance;
- vary catalogue record versions and timestamps where a data source supports such history, or use clearly labelled controlled perturbations if it does not;
- distinguish observed interaction facts from user-confirmed preferences and model-inferred profile attributes;
- compare claim support, contradiction, unsupported-claim, and abstention rates as well as recommendation metrics.

The experiments must not claim that synthetic corruption is naturally occurring data drift. Report controlled perturbations as controlled stress tests.

## Candidate metrics

Recommendation:
- MAP@12 for the H&M next-purchase benchmark reference;
- NDCG@K / Recall@K with predeclared candidate and relevance definitions;
- hard-constraint violation rate;
- catalogue coverage and intra-list diversity;
- latency and memory.

Evidence and explanations:
- claim-level evidence-support precision;
- contradiction rate;
- unsupported-claim rate;
- abstention rate and appropriate-abstention rate;
- source/provenance trace completeness;
- stale-source and conflicting-source detection performance;
- counterfactual consistency under controlled change to a cited evidence record.

No single LLM judge should be treated as ground truth. Separate automatic evidence checks, NLI/LLM-assisted evaluation, and human evaluation. Any human study needs ethics approval/determination, a fixed protocol and consent.

## Required paper-reading order

1. **KAPER (2026)** — closest current graph-path evidence / LLM recommender; obtain and read full paper, identify datasets, path extraction, evaluation and limitations.
2. **G-Refer (WWW 2025)** — graph retrieval and evidence translation; inspect code and dataset compatibility.
3. **K-RagRec (ACL 2025)** — KG retrieval for recommendation; compare what relation structure is retrieved and whether evidence is verifiable.
4. **Kabongo & Guigue (PAKDD 2026)** — claim-level factual consistency evaluation; determine exact overlap with the verifier and metrics.
5. **ReasoningRec (NAACL 2025)** — Caverlee-group method; review actual code, prompts, preference modelling and datasets.
6. **LangPTune (CIKM 2025)** — Cornell fit; analyse the difference between optimised language profiles and source-grounded evidence.
7. **LLM-powered subgraph reasoning (KBS 2025)** and **PC-CRS (EMNLP 2024)** — adjacent methods in graph explanation and explanation credibility.
8. **XRec (EMNLP 2024)** — broad LLM explanation baseline and prior art.

## Reproducible review template

For every paper, record:
- exact bibliographic citation and venue/version;
- research question and contribution;
- user/item data and access terms;
- representation and model architecture;
- baseline conditions;
- recommendation and explanation metrics;
- whether explanations are grounded in source records or merely graph paths/profile text;
- how contradiction, stale evidence, missing attributes and uncertainty are handled;
- what code and data can be legally reproduced;
- what is directly comparable with OGE-Fashion;
- what remains untested.

## Starting links

- XRec: https://aclanthology.org/2024.findings-emnlp.22/
- PC-CRS: https://aclanthology.org/2024.findings-emnlp.247/
- ReasoningRec: https://aclanthology.org/2025.findings-naacl.454/
- G-Refer: https://researchportal.hkust.edu.hk/en/publications/g-refer-graph-retrieval-augmented-large-language-model-for-explai/
- K-RagRec: https://aclanthology.org/2025.acl-long.1317/
- Subgraph reasoning: https://doi.org/10.1016/j.knosys.2025.114307
- LangPTune: https://doi.org/10.1145/3746252.3761369
- Knowledge-aware conversational explanations: https://doi.org/10.1007/s11257-025-09432-6
- Factual consistency: https://doi.org/10.1007/978-981-92-1465-5_2
- KAPER: https://doi.org/10.1016/j.knosys.2026.116236

This matrix is a focused scoping review, not proof of novelty or systematic-review coverage. It must be expanded using backward/forward citation tracing and a reproducible database search before a manuscript or novelty claim.
