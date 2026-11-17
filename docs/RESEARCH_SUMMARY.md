# OGE-Fashion — Research Summary

## Structured abstract

**Background:** Fashion and beauty recommenders may rank attribute-similar items while violating explicit context or style constraints. Explanations are difficult to audit when supporting evidence is not represented explicitly.

**Objective:** OGE-Fashion investigates whether a provenance-aware OWL ontology, SHACL data constraints and SPARQL-executable rules can improve constraint satisfaction and explanation traceability relative to a non-ontology attribute-matching baseline.

**Methods:** The 2026 extension models profiles, preferences, contexts, fashion/makeup entities, attributes, compatibility assessments, recommendation results and evidence. Fashionpedia taxonomy records retain source identifiers and provenance. Validation uses RDF/Turtle checks, HermiT consistency reasoning, SPARQL competency queries and SHACL. A deterministic synthetic benchmark compares a weighted colour/attribute baseline with a SPARQL-filtered condition on the same held-out profiles.

**Current results:** The ontology branch passed structural validation (3,237 RDF triples), HermiT consistency checks, 12/12 synthetic SPARQL tests, 4/4 SHACL positive/negative tests and the existing 15/15 foundation shade unit tests. The synthetic benchmark results are below and in [the full evaluation report](../results/evaluation_summary.md).

**Conclusion:** The current work establishes a reproducible semantic model and a small software-level demonstration. It does not establish real-world recommendation benefit or human-perceived explanation usefulness.

## Provenance

The historical BS Software Engineering FYP at the University of Sargodha ran **November 2023–May 2024**. The OWL/Turtle ontology, SHACL constraints, SPARQL competency tests, HermiT validation and recommender benchmark belong to the **2026 research extension**. Later work is not backdated.

## Architecture

~~~mermaid
flowchart TD
    A[Source vocabularies<br/>Fashionpedia taxonomy] --> B[Provenance-aware OWL ontology]
    C[Synthetic profile<br/>preferences and context] --> D[SPARQL constraint filtering]
    B --> D
    E[Synthetic item catalogue<br/>attributes and colour] --> D
    D --> F[Candidate set]
    F --> G[Shared attribute and colour ranking]
    G --> H[Ranked recommendations]
    H --> I[Structured explanation traces]
    B --> J[HermiT consistency checks]
    B --> K[SHACL data constraints]
    B --> L[SPARQL competency tests]
~~~

## Reproduction and CLI demo

~~~bash
python -m pip install -r requirements-research.txt
python experiments/evaluate_recommender.py
python experiments/evaluate_recommender.py --demo
~~~

Example explanation-trace shape:

~~~json
{
  "profile_id": "synthetic-02",
  "recommendations": [
    {
      "item_id": "item03",
      "trace": [
        {"property": "oge:hasOccasion", "requested": "office", "item_value": "office", "status": "satisfied"},
        {"property": "oge:hasStyle (dress-code)", "requested": "formal", "item_value": "formal", "status": "satisfied"},
        {"property": "oge:hasStyle (style)", "requested": "minimal", "item_value": "minimal", "status": "satisfied"},
        {"property": "oge:hasColour", "status": "soft_ranking_signal"}
      ]
    }
  ]
}
~~~

The CLI prints the full generated trace, including the reference colour and distance.

## Synthetic benchmark results

| Metric | A: non-ontology baseline | B: SPARQL/ontology-guided | B − A |
|---|---:|---:|---:|
| Precision@3 | 0.6667 | 0.7778 | +0.1111 |
| Recall@3 | 0.8889 | 1.0000 | +0.1111 |
| NDCG@3 | 0.9218 | 1.0000 | +0.0782 |
| Constraint satisfaction rate | 0.6667 | 1.0000 | +0.3333 |
| Explanation trace coverage | 0.0000 | 1.0000 | +1.0000 |

**Interpretation boundary:** 24 constructed profiles were generated; 6 held-out profiles were evaluated using seed 20261117 and a catalogue of 18 synthetic items. Relevance labels are generated from the same occasion, dress-code, style and colour fields used by the constraint rules. These results demonstrate designed filtering behaviour on this fixture, not independent evidence of improved recommendations for real people. Trace coverage measures trace presence, not explanation quality.

## Limitations and next research

- Synthetic profiles/catalogue only; no user data or observed preference labels.
- Synthetic undertone labels are not measurements or computer-vision predictions.
- Colour ranking uses encoded-sRGB Euclidean distance, not a validated skin-tone or foundation method.
- SPARQL rules are operationalised constraints aligned with OGE properties; HermiT is not used for per-request inference.
- Facial-image computer-vision classification, human user studies, learned recommendation models, real-data evaluation and peer-reviewed publication are future work.
- Dataset image rights and some metadata reuse conditions remain source-specific and must be checked before reuse.
