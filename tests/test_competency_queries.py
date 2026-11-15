from __future__ import annotations

import re
import unittest
from pathlib import Path

from rdflib import Graph, Namespace

ROOT = Path(__file__).resolve().parents[1]
OGE = Namespace("https://w3id.org/oge-fashion/ontology#")


def load_queries(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    blocks = re.findall(r"(?ms)^# BEGIN ([A-Z0-9_]+)\n(.*?)^# END \1\s*$", content)
    queries = {name: query.strip() for name, query in blocks}
    if len(queries) != 12:
        raise AssertionError(f"Expected 12 competency query blocks, found {len(queries)}")
    return queries


class CompetencyQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = Graph()
        cls.graph.parse(ROOT / "ontology" / "oge-fashion-v0.1.ttl", format="turtle")
        cls.graph.parse(ROOT / "tests" / "fixtures" / "competency-example.ttl", format="turtle")
        cls.queries = load_queries(ROOT / "ontology" / "queries" / "competency-questions.rq")

    @classmethod
    def rows(cls, query_name: str) -> list[tuple[str, ...]]:
        results = cls.graph.query(cls.queries[query_name])
        return [tuple(str(value) for value in row) for row in results]

    def test_cq01_fashion_preferences(self) -> None:
        rows = self.rows("CQ01_FASHION_PREFERENCES")
        self.assertEqual(len(rows), 1)
        self.assertIn("CasualStyle", rows[0][1])

    def test_cq02_makeup_preferences(self) -> None:
        rows = self.rows("CQ02_MAKEUP_PREFERENCES")
        self.assertEqual(len(rows), 1)
        self.assertIn("RoseColour", rows[0][1])

    def test_cq03_hard_exclusions(self) -> None:
        rows = self.rows("CQ03_HARD_EXCLUSIONS")
        self.assertEqual(len(rows), 1)
        self.assertIn("blackDressA", rows[0][0])

    def test_cq04_budget_and_occasion(self) -> None:
        rows = self.rows("CQ04_BUDGET_AND_OCCASION")
        self.assertEqual(len(rows), 1)
        self.assertIn("officeOccasion", rows[0][0])
        self.assertEqual(rows[0][1:], ("80.0", "EUR"))

    def test_cq05_profile_assertion_origin(self) -> None:
        rows = self.rows("CQ05_PROFILE_ASSERTION_ORIGIN")
        origins = {row[1] for row in rows}
        self.assertEqual(origins, {"user-confirmed", "model-inferred"})
        confirmation = {row[1]: row[2] for row in rows}
        self.assertEqual(confirmation["user-confirmed"], "true")
        self.assertEqual(confirmation["model-inferred"], "false")

    def test_cq06_fashion_category(self) -> None:
        rows = self.rows("CQ06_FASHION_CATEGORY")
        self.assertEqual(len(rows), 1)
        self.assertIn("shirtA", rows[0][0])

    def test_cq07_makeup_attributes(self) -> None:
        rows = self.rows("CQ07_MAKEUP_ATTRIBUTES")
        self.assertEqual(len(rows), 1)
        self.assertIn("lipstickA", rows[0][0])
        self.assertIn("RoseColour", rows[0][1])
        self.assertIn("MatteFinish", rows[0][2])

    def test_cq08_missing_required_attribute_is_unknown(self) -> None:
        rows = self.rows("CQ08_MISSING_REQUIRED_ATTRIBUTE")
        candidates = {row[0] for row in rows}
        self.assertTrue(any("blackDressA" in item for item in candidates))
        self.assertTrue(any("unknownMaterialJacket" in item for item in candidates))
        self.assertFalse(any("shirtA" in item for item in candidates))

    def test_cq09_compatibility_has_evidence(self) -> None:
        rows = self.rows("CQ09_COMPATIBILITY_WITH_EVIDENCE")
        self.assertEqual(len(rows), 1)
        self.assertIn("shirtLipstickAssessment", rows[0][0])
        self.assertIn("syntheticColourEvidence", rows[0][3])

    def test_cq10_explanation_is_traceable(self) -> None:
        rows = self.rows("CQ10_EXPLANATION_TRACEABILITY")
        self.assertGreaterEqual(len(rows), 1)
        self.assertTrue(any("fashionStylePreference" in row[1] for row in rows))
        self.assertTrue(any("shirtLipstickAssessment" in row[3] for row in rows))
        self.assertTrue(any("syntheticColourEvidence" in row[4] for row in rows))

    def test_cq11_learned_model_signal_is_identified(self) -> None:
        rows = self.rows("CQ11_LEARNED_MODEL_COMPONENT")
        self.assertEqual(len(rows), 1)
        self.assertIn("synthetic-learned-ranker", rows[0][1])
        self.assertEqual(rows[0][2], "0.74")

    def test_cq12_insufficient_evidence_is_reported(self) -> None:
        rows = self.rows("CQ12_INSUFFICIENT_EVIDENCE")
        self.assertEqual(len(rows), 1)
        self.assertIn("insufficientEvidenceExplanation", rows[0][0])
        self.assertIn("unverifiedAssessment", rows[0][2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
