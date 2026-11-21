"""Illustrative evidence-checking demo; no LLM is called."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from oge_fashion.explanation_verifier import (  # noqa: E402
    EvidenceOrigin,
    EvidenceRecord,
    ExplanationClaim,
    verify_claims,
)


def main() -> None:
    evidence = [
        EvidenceRecord("pref-01", "user-01", "prefers-style", "classic", EvidenceOrigin.USER_CONFIRMED),
        EvidenceRecord("item-01", "item-01", "primary-material", "cotton", EvidenceOrigin.CATALOGUE_VERIFIED, True),
        EvidenceRecord("item-02", "item-01", "primary-finish", "glossy", EvidenceOrigin.CATALOGUE_VERIFIED, True),
        EvidenceRecord("synthetic-01", "synthetic-user-01", "prefers-style", "relaxed", EvidenceOrigin.SYNTHETIC_FIXTURE),
        EvidenceRecord("synthetic-02", "synthetic-item-01", "primary-material", "cotton", EvidenceOrigin.SYNTHETIC_FIXTURE, True),
    ]
    claims = [
        ExplanationClaim("user-01", "prefers-style", "classic", ("pref-01",)),
        ExplanationClaim("item-01", "primary-material", "silk", ("item-01",)),
        ExplanationClaim("item-01", "primary-finish", "matte", ("item-02",)),
        ExplanationClaim("item-01", "has-colour", "burgundy", ()),
        ExplanationClaim("synthetic-user-01", "prefers-style", "relaxed", ("synthetic-01",)),
        ExplanationClaim("synthetic-item-01", "primary-material", "silk", ("synthetic-02",)),
    ]
    results = verify_claims(claims, evidence)
    payload = [
        {"claim": claim.__dict__, "verification": result.to_dict()}
        for claim, result in zip(claims, results, strict=True)
    ]
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
