"""Fail-closed verification of explanation claims against cited evidence.

This module does not generate explanations or call an LLM. It checks whether
an already-produced claim is supported by the evidence records it cites.
Synthetic fixtures are reported separately from verified evidence so a demo
cannot be mistaken for real-world validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class EvidenceOrigin(str, Enum):
    USER_CONFIRMED = "user-confirmed"
    CATALOGUE_VERIFIED = "catalogue-verified"
    SYSTEM_RECORDED = "system-recorded"
    MODEL_INFERRED = "model-inferred"
    SYNTHETIC_FIXTURE = "synthetic-fixture"


class VerificationStatus(str, Enum):
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    CONTRADICTED_IN_FIXTURE = "contradicted-in-synthetic-fixture"
    UNSUPPORTED = "unsupported"
    UNVERIFIED = "unverified"
    SUPPORTED_IN_FIXTURE = "supported-in-synthetic-fixture"


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    subject: str
    predicate: str
    value: str
    origin: EvidenceOrigin
    is_single_valued: bool = False

    def __post_init__(self) -> None:
        for field_name in ("evidence_id", "subject", "predicate", "value"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not isinstance(self.origin, EvidenceOrigin):
            raise ValueError("origin must be an EvidenceOrigin value")
        if not isinstance(self.is_single_valued, bool):
            raise ValueError("is_single_valued must be a bool")


@dataclass(frozen=True)
class ExplanationClaim:
    subject: str
    predicate: str
    value: str
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("subject", "predicate", "value"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not isinstance(self.evidence_ids, tuple):
            raise ValueError("evidence_ids must be a tuple of strings")
        if any(not isinstance(item, str) or not item.strip() for item in self.evidence_ids):
            raise ValueError("evidence_ids must contain non-empty strings")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("evidence_ids must not contain duplicates")


@dataclass(frozen=True)
class VerificationResult:
    status: VerificationStatus
    reason: str
    cited_evidence_ids: tuple[str, ...]
    matching_evidence_ids: tuple[str, ...] = ()
    conflicting_evidence_ids: tuple[str, ...] = ()
    unknown_evidence_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "cited_evidence_ids": list(self.cited_evidence_ids),
            "matching_evidence_ids": list(self.matching_evidence_ids),
            "conflicting_evidence_ids": list(self.conflicting_evidence_ids),
            "unknown_evidence_ids": list(self.unknown_evidence_ids),
        }


def _normalise(value: str) -> str:
    """Normalise whitespace and case only; do not perform semantic matching."""
    return " ".join(value.split()).casefold()


def _index_evidence(records: Iterable[EvidenceRecord]) -> dict[str, EvidenceRecord]:
    index: dict[str, EvidenceRecord] = {}
    for record in records:
        if not isinstance(record, EvidenceRecord):
            raise TypeError("records must contain EvidenceRecord instances")
        if record.evidence_id in index:
            raise ValueError(f"Duplicate evidence_id: {record.evidence_id}")
        index[record.evidence_id] = record
    return index


def verify_claim(
    claim: ExplanationClaim,
    evidence_records: Iterable[EvidenceRecord],
) -> VerificationResult:
    """Verify one claim using only evidence IDs explicitly cited by the claim.

    Trusted origins may support or contradict a claim. Model-inferred records
    are never treated as verified evidence. Synthetic fixture records can only
    produce a synthetic-fixture result, never a real-world supported result.
    A missing/unknown citation fails closed as unsupported.

    Important: origin labels and the single-valued flag are supplied by the
    calling application. This prototype does not authenticate sources or
    validate cardinality against the OWL ontology.
    """
    if not isinstance(claim, ExplanationClaim):
        raise TypeError("claim must be an ExplanationClaim instance")

    index = _index_evidence(evidence_records)
    if not claim.evidence_ids:
        return VerificationResult(
            status=VerificationStatus.UNSUPPORTED,
            reason="The claim cites no evidence records.",
            cited_evidence_ids=(),
        )

    unknown = tuple(item for item in claim.evidence_ids if item not in index)
    if unknown:
        return VerificationResult(
            status=VerificationStatus.UNSUPPORTED,
            reason="At least one cited evidence ID does not exist in the supplied evidence set.",
            cited_evidence_ids=claim.evidence_ids,
            unknown_evidence_ids=unknown,
        )

    cited = [index[item] for item in claim.evidence_ids]
    relevant = [
        record for record in cited
        if _normalise(record.subject) == _normalise(claim.subject)
        and _normalise(record.predicate) == _normalise(claim.predicate)
    ]
    if not relevant:
        return VerificationResult(
            status=VerificationStatus.UNSUPPORTED,
            reason="Cited records do not describe the claim's subject and predicate.",
            cited_evidence_ids=claim.evidence_ids,
        )

    trusted = [r for r in relevant if r.origin in {
        EvidenceOrigin.USER_CONFIRMED,
        EvidenceOrigin.CATALOGUE_VERIFIED,
        EvidenceOrigin.SYSTEM_RECORDED,
    }]
    synthetic = [r for r in relevant if r.origin is EvidenceOrigin.SYNTHETIC_FIXTURE]
    inferred = [r for r in relevant if r.origin is EvidenceOrigin.MODEL_INFERRED]
    claim_value = _normalise(claim.value)

    matching_trusted = [r for r in trusted if _normalise(r.value) == claim_value]
    conflicting_trusted = [
        r for r in trusted
        if r.is_single_valued and _normalise(r.value) != claim_value
    ]
    matching_synthetic = [r for r in synthetic if _normalise(r.value) == claim_value]
    conflicting_synthetic = [
        r for r in synthetic
        if r.is_single_valued and _normalise(r.value) != claim_value
    ]
    matching_inferred = [r for r in inferred if _normalise(r.value) == claim_value]

    if conflicting_trusted:
        reason = "Verified evidence contains a conflicting value for the same subject and predicate."
        if matching_trusted:
            reason += " The cited evidence set is internally inconsistent."
        return VerificationResult(
            status=VerificationStatus.CONTRADICTED,
            reason=reason,
            cited_evidence_ids=claim.evidence_ids,
            matching_evidence_ids=tuple(r.evidence_id for r in matching_trusted),
            conflicting_evidence_ids=tuple(r.evidence_id for r in conflicting_trusted),
        )

    if matching_trusted:
        return VerificationResult(
            status=VerificationStatus.SUPPORTED,
            reason="The claim exactly matches cited user-confirmed, catalogue-verified, or system-recorded evidence.",
            cited_evidence_ids=claim.evidence_ids,
            matching_evidence_ids=tuple(r.evidence_id for r in matching_trusted),
        )

    if conflicting_synthetic:
        return VerificationResult(
            status=VerificationStatus.CONTRADICTED_IN_FIXTURE,
            reason="The claim conflicts with the supplied synthetic fixture; this is not a real-world finding.",
            cited_evidence_ids=claim.evidence_ids,
            conflicting_evidence_ids=tuple(r.evidence_id for r in conflicting_synthetic),
        )

    if matching_synthetic:
        return VerificationResult(
            status=VerificationStatus.SUPPORTED_IN_FIXTURE,
            reason="The claim matches synthetic test data only; it is not evidence about real users or products.",
            cited_evidence_ids=claim.evidence_ids,
            matching_evidence_ids=tuple(r.evidence_id for r in matching_synthetic),
        )

    if inferred:
        return VerificationResult(
            status=VerificationStatus.UNVERIFIED,
            reason="The cited record is model-inferred and cannot independently verify an explanation claim.",
            cited_evidence_ids=claim.evidence_ids,
        )

    return VerificationResult(
        status=VerificationStatus.UNSUPPORTED,
        reason="No cited record supports the claim.",
        cited_evidence_ids=claim.evidence_ids,
    )


def verify_claims(
    claims: Iterable[ExplanationClaim],
    evidence_records: Iterable[EvidenceRecord],
) -> list[VerificationResult]:
    """Verify multiple claims against one evidence set."""
    evidence = tuple(evidence_records)
    _index_evidence(evidence)  # Validate once, including duplicate IDs.
    return [verify_claim(claim, evidence) for claim in claims]
