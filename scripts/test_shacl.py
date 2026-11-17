from __future__ import annotations

import unittest

from pyshacl import validate
from rdflib import Graph, Literal, Namespace, RDF, XSD

ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
OGE = Namespace("https://w3id.org/oge-fashion/ontology#")
SH = Namespace("http://www.w3.org/ns/shacl#")


def load_graph() -> Graph:
    graph = Graph()
    graph.parse(ROOT / "ontology" / "oge-fashion-v0.1.ttl", format="turtle")
    graph.parse(ROOT / "tests" / "fixtures" / "competency-example.ttl", format="turtle")
    return graph


def validate_graph(graph: Graph):
    shapes = Graph()
    shapes.parse(ROOT / "ontology" / "shapes" / "oge-fashion-shapes.ttl", format="turtle")
    return validate(
        data_graph=graph,
        shacl_graph=shapes,
        inference="rdfs",
        meta_shacl=True,
        advanced=True,
        abort_on_first=False,
    )


class SHACLValidationTests(unittest.TestCase):
    def test_synthetic_fixture_conforms(self) -> None:
        graph = load_graph()
        conforms, report, text = validate_graph(graph)
        self.assertTrue(conforms, text)

    def test_preference_requires_exactly_one_value(self) -> None:
        graph = load_graph()
        invalid = OGE.invalidPreferenceMissingValue
        graph.add((invalid, RDF.type, OGE.Preference))
        graph.add((invalid, OGE.preferenceAbout, OGE.StyleConceptField))
        graph.add((invalid, OGE.preferenceDomain, Literal("fashion")))
        graph.add((invalid, OGE.preferencePolarity, Literal("positive")))
        conforms, report, text = validate_graph(graph)
        self.assertFalse(conforms, "A Preference without preferenceValue should fail SHACL.")
        self.assertTrue(
            any(str(v).endswith("invalidPreferenceMissingValue") for v in report.objects(None, SH.focusNode)),
            text,
        )

    def test_supported_explanation_requires_evidence(self) -> None:
        graph = load_graph()
        invalid = OGE.invalidSupportedExplanation
        graph.add((invalid, RDF.type, OGE.Explanation))
        graph.add((invalid, OGE.explains, OGE.shirtResult))
        graph.add((invalid, OGE.explanationStatus, Literal("supported")))
        graph.add((invalid, OGE.explanationMessage, Literal("This test explanation lacks evidence.")))
        conforms, report, text = validate_graph(graph)
        self.assertFalse(conforms, "A supported explanation without evidence should fail SHACL.")
        self.assertTrue(
            any(str(v).endswith("invalidSupportedExplanation") for v in report.objects(None, SH.focusNode)),
            text,
        )

    def test_insufficient_evidence_explanation_is_valid_without_evidence(self) -> None:
        graph = load_graph()
        conforms, report, text = validate_graph(graph)
        self.assertTrue(conforms, "The synthetic insufficient-evidence explanation should conform: "+text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
