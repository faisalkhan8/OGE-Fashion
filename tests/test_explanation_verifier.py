import unittest

from oge_fashion.explanation_verifier import (
    EvidenceOrigin,
    EvidenceRecord,
    ExplanationClaim,
    VerificationStatus,
    verify_claim,
    verify_claims,
)


class ExplanationVerifierTests(unittest.TestCase):
    def setUp(self):
        self.evidence = [
            EvidenceRecord("pref-01", "user-01", "prefers-style", "classic", EvidenceOrigin.USER_CONFIRMED),
            EvidenceRecord("item-01", "item-01", "primary-material", "cotton", EvidenceOrigin.CATALOGUE_VERIFIED, True),
            EvidenceRecord("item-02", "item-01", "primary-finish", "glossy", EvidenceOrigin.CATALOGUE_VERIFIED, True),
            EvidenceRecord("model-01", "user-01", "prefers-style", "minimal", EvidenceOrigin.MODEL_INFERRED),
            EvidenceRecord("synthetic-01", "synthetic-user-01", "prefers-style", "relaxed", EvidenceOrigin.SYNTHETIC_FIXTURE),
        ]

    def test_user_confirmed_claim_is_supported(self):
        result = verify_claim(
            ExplanationClaim("user-01", "prefers-style", "classic", ("pref-01",)), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.SUPPORTED)

    def test_catalogue_claim_is_supported(self):
        result = verify_claim(
            ExplanationClaim("item-01", "primary-material", "cotton", ("item-01",)), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.SUPPORTED)

    def test_whitespace_and_case_are_normalised(self):
        result = verify_claim(
            ExplanationClaim(" USER-01 ", "PREFERS-STYLE", " Classic  ", ("pref-01",)), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.SUPPORTED)

    def test_conflicting_verified_value_is_contradicted(self):
        result = verify_claim(
            ExplanationClaim("item-01", "primary-finish", "matte", ("item-02",)), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.CONTRADICTED)
        self.assertEqual(result.conflicting_evidence_ids, ("item-02",))

    def test_claim_without_evidence_is_unsupported(self):
        result = verify_claim(
            ExplanationClaim("item-01", "has-colour", "burgundy", ()), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.UNSUPPORTED)

    def test_unknown_citation_fails_closed(self):
        result = verify_claim(
            ExplanationClaim("user-01", "prefers-style", "classic", ("missing-id",)), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.UNSUPPORTED)
        self.assertEqual(result.unknown_evidence_ids, ("missing-id",))

    def test_wrong_subject_or_predicate_does_not_support_claim(self):
        result = verify_claim(
            ExplanationClaim("item-02", "has-material", "cotton", ("item-01",)), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.UNSUPPORTED)

    def test_model_inference_is_not_verification(self):
        result = verify_claim(
            ExplanationClaim("user-01", "prefers-style", "minimal", ("model-01",)), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.UNVERIFIED)

    def test_synthetic_evidence_is_labelled_separately(self):
        result = verify_claim(
            ExplanationClaim("synthetic-user-01", "prefers-style", "relaxed", ("synthetic-01",)), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.SUPPORTED_IN_FIXTURE)

    def test_synthetic_conflict_is_not_labelled_as_real_contradiction(self):
        fixture = self.evidence + [
            EvidenceRecord("synthetic-02", "synthetic-item-01", "primary-material", "cotton", EvidenceOrigin.SYNTHETIC_FIXTURE, True)
        ]
        result = verify_claim(
            ExplanationClaim("synthetic-item-01", "primary-material", "silk", ("synthetic-02",)), fixture
        )
        self.assertEqual(result.status, VerificationStatus.CONTRADICTED_IN_FIXTURE)

    def test_verified_conflict_overrides_a_match(self):
        contradictory = self.evidence + [
            EvidenceRecord("pref-02", "user-01", "primary-style", "minimal", EvidenceOrigin.USER_CONFIRMED, True),
            EvidenceRecord("pref-03", "user-01", "primary-style", "classic", EvidenceOrigin.USER_CONFIRMED, True)
        ]
        result = verify_claim(
            ExplanationClaim("user-01", "primary-style", "classic", ("pref-02", "pref-03")), contradictory
        )
        self.assertEqual(result.status, VerificationStatus.CONTRADICTED)
        self.assertIn("internally inconsistent", result.reason)

    def test_non_single_valued_property_is_not_declared_contradicted(self):
        result = verify_claim(
            ExplanationClaim("user-01", "prefers-style", "minimal", ("pref-01",)), self.evidence
        )
        self.assertEqual(result.status, VerificationStatus.UNSUPPORTED)

    def test_duplicate_evidence_ids_are_rejected(self):
        duplicate = self.evidence + [self.evidence[0]]
        with self.assertRaises(ValueError):
            verify_claims([], duplicate)

    def test_duplicate_claim_citations_are_rejected(self):
        with self.assertRaises(ValueError):
            ExplanationClaim("user-01", "prefers-style", "classic", ("pref-01", "pref-01"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
