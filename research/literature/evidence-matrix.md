# Literature Evidence Matrix — OGE-Fashion
**Review snapshot:** 2026-11-15  
**Version:** 0.1 — focused preliminary scoping review, not a completed systematic review  
**Purpose:** establish what is already known, identify relevant baselines, and frame a defensible research gap for subsequent screening.

## 1. Search scope and method

This first pass used targeted searches for:
- fashion recommendation and outfit compatibility;
- explainable fashion recommendation;
- makeup/cosmetics recommendation;
- knowledge-based, ontology-based, and hybrid recommendation;
- context-aware recommendation and recommendation explanations.

The search was targeted across publisher/venue pages, institutional research portals, W3C, PubMed, and dataset-owner pages. The searches were conducted on 15 November 2026. Query examples:
- "fashion recommendation survey computational technologies";
- "explainable fashion compatibility modeling review";
- "outfit compatibility transformer fashion recommendation";
- "makeup recommendation rules deep neural network";
- "cosmetics product recommendation ingredients deep learning";
- "knowledge-based recommender systems overview research directions";
- "context-aware recommender systems systematic literature review";
- "explainable recommendation large language models review".

### Inclusion approach
Included sources were selected because they are directly related to at least one of the OGE-Fashion domains or methodological components, and had an identifiable publisher, conference, journal, institutional, or standards page. Survey papers, primary research papers, and standards are distinguished.

### Exclusions / limitations
This is not a systematic literature review: no exhaustive database export, duplicate screening, independent reviewer screening, or formal PRISMA flow has been completed. Search-engine coverage can be incomplete. Some publisher full texts were not accessible during this first pass; those entries rely on authoritative abstracts/metadata pages. The matrix must be expanded through ACM Digital Library, IEEE Xplore, Scopus/Web of Science or available institutional access, SpringerLink, PubMed, and relevant conference proceedings before making a publication-level novelty claim.

## 2. Evidence matrix

| ID | Source | Type / domain | Methods or focus reported by source | Relevance to OGE-Fashion | Limitation / implication for our design |
|---|---|---|---|---|---|
| L1 | Ding et al. (2024), *Computational Technologies for Fashion Recommendation: A Survey*, ACM Computing Surveys 56(5), Article 121. DOI: [10.1145/3627100](https://doi.org/10.1145/3627100) | Peer-reviewed survey; fashion recommendation | Reviews fashion recommendation tasks including personalised product recommendation, complementary/mix-and-match, and outfit recommendation; categorises tasks, formulations, methods, datasets, and limitations. | Establishes the fashion task landscape and gives a starting map of candidate baselines and datasets. | Generic fashion recommendation is already a mature survey topic. Our contribution must be a precise research question beyond building another fashion recommender. |
| L2 | Selwon & Szymański (2024), *A Review of Explainable Fashion Compatibility Modeling Methods*, ACM Computing Surveys 56(11), pp. 1–29. DOI: [10.1145/3664614](https://doi.org/10.1145/3664614) | Peer-reviewed survey; explainable fashion compatibility | Reviews fashion compatibility methods through reproducibility, explainability, and novelty; surveys available datasets; discusses representation bias, sustainability, and explainable model assessment. | Directly informs explanation evaluation, dataset selection, and bias analysis for fashion compatibility. | Explainable fashion compatibility is not itself a novel claim. We should identify the specific gap in ontology-grounded, cross-domain explanation and compare against existing fashion explainability methods. |
| L3 | Sarkar et al. (2022), *OutfitTransformer: Outfit Representations for Fashion Recommendation*, CVPR Workshops, pp. 2262–2266. DOI: [10.1109/CVPRW56347.2022.00249](https://doi.org/10.1109/CVPRW56347.2022.00249). [CVF paper page](https://openaccess.thecvf.com/content/CVPR2022W/CVFAD/html/Sarkar_OutfitTransformer_Outfit_Representations_for_Fashion_Recommendation_CVPRW_2022_paper.html) | Primary research; fashion compatibility/retrieval | Represents an outfit as an unordered set, uses self-attention, and applies a set-wise outfit ranking loss to learn outfit compatibility and retrieve complementary items. | Candidate ML baseline/reference for compatibility and complementary-item retrieval. | Its reported focus is learned compatibility and retrieval, not our proposed shared fashion/makeup ontology. Need compare task definitions and dataset protocol rather than claim direct superiority. |
| L4 | Alashkar et al. (2017), *Examples-Rules Guided Deep Neural Network for Makeup Recommendation*, AAAI 31(1). DOI: [10.1609/aaai.v31i1.10626](https://doi.org/10.1609/aaai.v31i1.10626) | Primary research; makeup recommendation | Describes facial-trait coding, before/after makeup image pairs, makeup-artist rules/knowledge, a neural recommendation model, and makeup synthesis; authors report statistical and perceptual evaluations. | Confirms that makeup recommendation using examples and expert rules/knowledge has prior precedent. Relevant to designing makeup-domain baselines and provenance for expert rules. | A claim that rule-guided makeup recommendation is new would be incorrect. The paper uses facial traits and a specialised dataset; our first phase should avoid face-image dependency and assess explicit user preferences separately. |
| L5 | Lee et al. (2024), *Deep learning-based skin care product recommendation: A focus on cosmetic ingredient analysis and facial skin conditions*, Journal of Cosmetic Dermatology 23(6), 2066–2077. DOI: [10.1111/jocd.16218](https://doi.org/10.1111/jocd.16218) | Primary research; skin-care product recommendation | Describes modelling ingredient sequences and combining product ingredient analysis with AI skin-condition analysis from frontal face images to produce personalised product recommendations. | Relevant adjacent work for cosmetic product metadata, ingredient attributes, and personalisation. | Skin-care efficacy/product recommendation is not the same task as makeup-look or colour/style recommendation. Do not treat it as direct evidence for makeup compatibility. Face analysis also introduces consent, privacy, and validation requirements. |
| L6 | Uta et al. (2024), *Knowledge-based recommender systems: overview and research directions*, Frontiers in Big Data 7:1304439. DOI: [10.3389/fdata.2024.1304439](https://doi.org/10.3389/fdata.2024.1304439) | Peer-reviewed review; knowledge-based recommendation | Reviews case-based, critiquing-based, constraint-based and related approaches; discusses semantic user preference knowledge, item knowledge, recommendation knowledge, machine-learning integration, preference elicitation, and evaluation. | Strong methodological foundation for representing explicit preferences/constraints and combining knowledge-based reasoning with learned recommendation. | Ontology/knowledge plus ML integration is already a recognised research direction. A generic hybrid approach cannot be claimed as novel. Need a domain-specific representation, operational contribution, and controlled evaluation. |
| L7 | Mateos & Bellogín (published online 2024; journal volume 2025), *A systematic literature review of recent advances on context-aware recommender systems*, Artificial Intelligence Review 58, Article 20. DOI: [10.1007/s10462-024-10939-4](https://doi.org/10.1007/s10462-024-10939-4) | Peer-reviewed systematic review; context-aware recommenders | Reviews use of context such as temporal, spatial, and social components in recommendation; the abstract notes lack of an agreed framework for context information and its integration. | Supports treating occasion and context as explicit recommendation inputs rather than incidental text fields. | Context-aware recommendation is itself well studied. Our contribution must define fashion/makeup-specific context semantics and demonstrate their value instead of claiming context-awareness is new. |
| L8 | Said (2025), *On explaining recommendations with Large Language Models: a review*, Frontiers in Big Data 7. DOI: [10.3389/fdata.2024.1505284](https://doi.org/10.3389/fdata.2024.1505284) | Mini-review; recommendation explanations | Review searched ACM Guide literature from ChatGPT's release through November 2024; its abstract reports 232 articles screened and six directly addressing LLM-based recommendation explanations. | Useful background on generated explanation work and its early evidence base at the review's cutoff. | Our initial explanation approach should be traceable to ontology paths, preferences, and recorded model-score components; an LLM should not invent explanation facts. This review is specifically LLM-focused and does not cover all explanation research. |
| L9 | W3C (2012), *OWL 2 Web Ontology Language — Document Overview, Second Edition*. [W3C Recommendation](https://www.w3.org/TR/owl2-overview/) | Standards document | Defines OWL 2 as a formal ontology language; introduces classes, properties, individuals, data values, semantics, profiles, and RDF exchange. | Authoritative technical basis for the ontology implementation and reasoner validation. | A standard is not evidence that a proposed ontology is useful or novel; the ontology must be evaluated against competency questions and data. |

## 3. Preliminary synthesis

### What is already established
1. Fashion recommendation spans personalised product recommendation, complementary-item recommendation, outfit recommendation, and compatibility modelling (L1).
2. Explainable fashion compatibility has already been surveyed, including dataset bias and explanation assessment (L2).
3. Learned outfit compatibility and retrieval models exist, including transformer/set-wise ranking approaches (L3).
4. Makeup recommendation has prior examples-and-rules neural approaches using facial traits and makeup-artist knowledge (L4).
5. Cosmetic product recommendation exists in adjacent skin-care settings using ingredient information and image-derived skin-condition features (L5).
6. Knowledge-based recommendation and its integration with machine learning are established broader research topics (L6).
7. Context-aware recommendation and explanation research are established fields (L7–L8).

### Preliminary gap candidate — not yet a novelty claim
The focused sources reviewed here motivate investigating whether a **single, explicit, modular ontology can represent shared user-controlled preferences and context across two related but distinct recommendation domains—fashion and makeup—and whether its relations can support evidence-traceable explanations in both domains**.

A narrower possible contribution is:
- a documented cross-domain conceptual model with separable fashion and makeup subdomains;
- preference/constraint and context representation that separates explicit user input from inferred model signals;
- explanation records grounded in ontology relations, item metadata, and named model score components;
- comparative evaluation of ontology-only, ML-only, and hybrid methods within each domain;
- a cross-domain outfit-plus-makeup use case only if suitable data and defensible labels can be obtained.

This gap is **provisional**. The current search does not establish that no comparable ontology or cross-domain system exists. We need a broader search including fashion ontologies, semantic product search, beauty/makeup recommender systems, knowledge graphs for cosmetics, and cross-category recommendation before claiming novelty.

## 4. Consequences for the research design

1. **Use separate domain evaluations first.** Fashion and makeup have different data sources and relevance definitions. Evaluate each domain separately before aggregating results.
2. **Treat cross-domain matching as a secondary experiment.** Do not claim that outfit–makeup combinations are better unless a labelled and defensible evaluation protocol exists.
3. **Retain four comparison conditions.** Content/item-feature baseline, ontology-only, ML-only, and hybrid.
4. **Make explanation correctness measurable.** Every explanation should resolve to a stored preference, item attribute, ontology relation, or score contribution.
5. **Do not require face images initially.** L4 and L5 illustrate face-image-based research but also reinforce the need to avoid assuming it is essential. Start with optional, user-confirmed attributes only if justified.
6. **Measure more than accuracy.** Evaluate constraints, coverage, diversity, latency, explanation quality, and known dataset representation limitations.
7. **Separate research and deployment data rights.** A dataset permitted for non-commercial experimentation may still be unsuitable for a public product.

## 5. Next literature-review tasks
- Expand search to semantic web/fashion ontology work and product knowledge graphs.
- Find and review the primary papers behind the fashion survey's key baseline categories.
- Identify more makeup/beauty recommender studies and separate makeup-look recommendation from skincare/cosmetic-product recommendation.
- Search for cross-domain fashion–beauty recommendation systems and ontology-guided explanations.
- Record full text review status, inclusion/exclusion rationale, and duplicate handling.
- Revise the candidate gap only after these steps.

## 6. References
1. Ding, Y., Zhihui, L. A. I., Mok, P. Y., & Chua, T. S. (2024). Computational Technologies for Fashion Recommendation: A Survey. *ACM Computing Surveys, 56*(5), Article 121. https://doi.org/10.1145/3627100
2. Selwon, K., & Szymański, J. (2024). A Review of Explainable Fashion Compatibility Modeling Methods. *ACM Computing Surveys, 56*(11), 1–29. https://doi.org/10.1145/3664614
3. Sarkar, R., Bodla, N., Vasileva, M. I., Lin, Y.-L., Beniwal, A., Lu, A., & Medioni, G. (2022). OutfitTransformer: Outfit Representations for Fashion Recommendation. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops*, 2262–2266. https://doi.org/10.1109/CVPRW56347.2022.00249.
4. Alashkar, T., Jiang, S., Wang, S., & Fu, Y. (2017). Examples-Rules Guided Deep Neural Network for Makeup Recommendation. *Proceedings of the AAAI Conference on Artificial Intelligence, 31*(1). https://doi.org/10.1609/aaai.v31i1.10626
5. Lee, J., Yoon, H., Kim, S., Lee, C., Lee, J., & Yoo, S. (2024). Deep learning-based skin care product recommendation: A focus on cosmetic ingredient analysis and facial skin conditions. *Journal of Cosmetic Dermatology, 23*(6), 2066–2077. https://doi.org/10.1111/jocd.16218
6. Uta, M., Felfernig, A., Le, V.-M., Tran, T. N. T., Garber, D., Lubos, S., & Burgstaller, T. (2024). Knowledge-based recommender systems: overview and research directions. *Frontiers in Big Data, 7*, 1304439. https://doi.org/10.3389/fdata.2024.1304439
7. Mateos, P., & Bellogín, A. (2025). A systematic literature review of recent advances on context-aware recommender systems. *Artificial Intelligence Review, 58*, 20. https://doi.org/10.1007/s10462-024-10939-4
8. Said, A. (2025). On explaining recommendations with Large Language Models: a review. *Frontiers in Big Data, 7*. https://doi.org/10.3389/fdata.2024.1505284
9. W3C. (2012). OWL 2 Web Ontology Language Document Overview (Second Edition). https://www.w3.org/TR/owl2-overview/

**Evidence boundary:** the summaries above are based on the cited publisher/venue/standards landing pages and available abstracts/metadata in this preliminary pass. Before manuscript writing, verify each citation against full text and confirm the exact claims, pages, and version.
