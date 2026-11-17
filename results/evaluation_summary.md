# Synthetic recommender benchmark — results

- Seed: 20261117; K: 3.
- Profiles: 24 generated; 6 held-out test profiles.
- Catalogue: 18 synthetic items.
- Split: deterministic 75/25 shuffled split; both conditions use identical held-out profiles.
- Test profile IDs: synthetic-02, synthetic-16, synthetic-01, synthetic-03, synthetic-08, synthetic-12.
- Relevance labels: exact occasion, dress-code and style match plus encoded-sRGB Euclidean colour distance <= 155.

| Metric | A: non-ontology baseline | B: SPARQL/ontology-guided | B − A |
|---|---:|---:|---:|
| Precision@3 | 0.6667 | 0.7778 | +0.1111 |
| Recall@3 | 0.8889 | 1.0000 | +0.1111 |
| NDCG@3 | 0.9218 | 1.0000 | +0.0782 |
| Constraint satisfaction rate | 0.6667 | 1.0000 | +0.3333 |
| Explanation trace coverage | 0.0000 | 1.0000 | +1.0000 |

## Interpretation

Both conditions use the same colour/attribute score. A ranks the full catalogue. B applies SPARQL filters using OGE hasOccasion and hasStyle assertions, then ranks the surviving items and attaches structured property-level traces.

Relevance labels are generated from the same synthetic fields used by the constraints. Differences are therefore implementation properties of this fixture, not independent evidence of improved recommendations for people. Trace coverage records trace presence, not human-perceived clarity or usefulness.

## Limitations

Deterministic synthetic benchmark only. Labels are generated from the same constructed fields used by the constraints. Results demonstrate implementation behaviour on this fixture; they do not establish real-world recommendation quality, user preference, generalisation, causal benefit or statistical significance.

- Profiles, reference colours and catalogue are synthetic; the undertone field is not inferred from a person.
- Colour distance is Euclidean distance in encoded sRGB, not CIEDE2000 or a validated skin-tone/foundation method.
- SPARQL rules are benchmark constraints aligned with OGE properties. HermiT is not invoked for per-request inference.
- No real users, observed preference labels, learned model, uncertainty intervals or statistical tests are involved.
- Dress-code and style labels are illustrative, not universal fashion rules.

Reproduce with: python experiments/evaluate_recommender.py (requires rdflib>=7.1,<8).
