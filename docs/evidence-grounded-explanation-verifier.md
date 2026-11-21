# Evidence-grounded explanation verifier (prototype)

## Purpose

This prototype checks whether an explanation claim exactly matches a cited record. It is a small research artefact for the proposed OGE-Fashion extension on faithful, constraint-aware explanations.

It does **not** call an LLM, generate explanations, validate a knowledge graph, or authenticate sources. The evidence records are supplied by a calling application.

## Status categories

| Status | Meaning |
|---|---|
| `supported` | Exact subject/predicate/value match against a record labelled user-confirmed, catalogue-verified, or system-recorded |
| `contradicted` | A conflicting value appears in cited trusted evidence and the caller marks that predicate as single-valued |
| `unsupported` | No usable cited evidence, an unknown evidence ID, or a subject/predicate mismatch |
| `unverified` | The only relevant evidence is model-inferred |
| `supported-in-synthetic-fixture` | Exact match against synthetic data only |
| `contradicted-in-synthetic-fixture` | Conflict occurs in synthetic data only |

Normalisation is deliberately limited to case-folding and whitespace. There is no semantic matching, entailment, ontology reasoning, or LLM judge.

## Minimal example

```python
from oge_fashion.explanation_verifier import (
    EvidenceOrigin, EvidenceRecord, ExplanationClaim, verify_claim
)

evidence = [
    EvidenceRecord(
        evidence_id="pref-01",
        subject="user-01",
        predicate="prefers-style",
        value="classic",
        origin=EvidenceOrigin.USER_CONFIRMED,
    )
]
claim = ExplanationClaim(
    subject="user-01",
    predicate="prefers-style",
    value="classic",
    evidence_ids=("pref-01",),
)
print(verify_claim(claim, evidence).to_dict())
```

Run the tests and example:

```bash
python -m unittest discover -s tests -v
python examples/evidence_verification_demo.py
```

## Design cautions

- Evidence-origin labels are assertions from the caller. The module does not establish that a record truly came from a user, product catalogue, or system log.
- The `is_single_valued` flag is caller-supplied metadata. It must be derived from a reviewed data/ontology schema; it must not be guessed by the language model.
- The module checks only cited evidence IDs. It does not search the full knowledge graph for omitted contradictory records.
- Exact string equality is intentionally conservative. It can reject equivalent values expressed with different vocabulary.
- A `supported` result means only that the claim matches the supplied record under this prototype's rules. It does not prove the source itself is factually correct.
- Synthetic results remain explicitly labelled as synthetic and must not be reported as real-user findings.

## Next validation steps

1. Map evidence records to stable IDs and provenance fields in the OGE-Fashion ontology.
2. Derive cardinality from a versioned schema rather than caller-set flags.
3. Add tests for stale, revoked, duplicate, and conflicting catalogue records.
4. Evaluate claim-level support and contradiction rates on an independently curated test set.
5. Compare structured/template explanations, LLM-only explanations, and evidence-conditioned explanations under the same tasks.
6. Obtain the required ethics determination before any human explanation study.

This prototype is a research implementation step, not a peer-reviewed result or evidence of improved user outcomes.
