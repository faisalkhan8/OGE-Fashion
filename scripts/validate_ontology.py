from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY_PATH = ROOT / "ontology" / "oge-fashion-v0.1.ttl"

OGE = Namespace("https://w3id.org/oge-fashion/ontology#")
SOURCE_URL = "https://github.com/KMnP/fashionpedia-api/blob/master/data/demo/category_attributes_descriptions.json"

EXPECTED_ATTRIBUTE_GROUPS = {
    "nickname": 153,
    "silhouette": 25,
    "waistline": 7,
    "length": 15,
    "neckline type": 25,
    "opening type": 10,
    "non-textile material type": 10,
    "leather": 4,
    "textile finishing, manufacturing techniques": 21,
    "textile pattern": 18,
    "animal": 6,
}
EXPECTED_CATEGORY_GROUPS = {
    "upperbody": 6,
    "lowerbody": 3,
    "wholebody": 4,
    "head": 3,
    "neck": 1,
    "arms and hands": 2,
    "waist": 1,
    "legs and feet": 4,
    "others": 3,
    "garment parts": 7,
    "closures": 2,
    "decorations": 10,
}


def values(graph: Graph, subject, predicate):
    return list(graph.objects(subject, predicate))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    graph = Graph()
    graph.parse(ONTOLOGY_PATH, format="turtle")

    ontology_nodes = list(graph.subjects(RDF.type, OWL.Ontology))
    require(len(ontology_nodes) == 1, f"Expected 1 ontology node, got {len(ontology_nodes)}")

    imported = [
        node for node in graph.subjects(OGE.sourceDataset, None)
        if values(graph, node, OGE.sourceTaxonomyID)
    ]
    require(len(imported) == 340, f"Expected 340 imported Fashionpedia records, got {len(imported)}")

    required_properties = [
        RDFS.label,
        OGE.sourceLocalID,
        OGE.sourceTaxonomyID,
        OGE.sourceSupercategory,
        OGE.sourceTaxonomyLevel,
        OGE.sourceDataset,
    ]
    for node in imported:
        for predicate in required_properties:
            found = values(graph, node, predicate)
            require(len(found) == 1, f"{node} must have exactly one {predicate}, found {len(found)}")
        require(
            str(values(graph, node, OGE.sourceDataset)[0]) == SOURCE_URL,
            f"{node} has an unexpected source manifest URL",
        )

    category_types = [
        OGE.MainApparelCategory,
        OGE.GarmentPartCategory,
        OGE.ClosureCategory,
        OGE.DecorationCategory,
    ]
    category_nodes = [n for n in imported if any((n, RDF.type, t) in graph for t in category_types)]
    attribute_nodes = [n for n in imported if (n, RDF.type, OGE.FashionpediaAttributeValue) in graph
                       or any((n, RDF.type, t) in graph for t in [
                           OGE.GarmentNicknameAttribute, OGE.GarmentSilhouetteAttribute,
                           OGE.WaistlineAttribute, OGE.GarmentLengthAttribute,
                           OGE.NecklineTypeAttribute, OGE.OpeningTypeAttribute,
                           OGE.NonTextileMaterialTypeAttribute, OGE.LeatherAttribute,
                           OGE.TextileFinishingTechniqueAttribute, OGE.TextilePatternAttribute,
                           OGE.AnimalPatternAttribute,
                       ])]
    require(len(category_nodes) == 46, f"Expected 46 category individuals, got {len(category_nodes)}")
    require(len(attribute_nodes) == 294, f"Expected 294 attribute individuals, got {len(attribute_nodes)}")

    category_groups = Counter(str(values(graph, n, OGE.sourceSupercategory)[0]) for n in category_nodes)
    attribute_groups = Counter(str(values(graph, n, OGE.sourceSupercategory)[0]) for n in attribute_nodes)
    require(dict(category_groups) == EXPECTED_CATEGORY_GROUPS, f"Category group counts differ: {dict(category_groups)}")
    require(dict(attribute_groups) == EXPECTED_ATTRIBUTE_GROUPS, f"Attribute group counts differ: {dict(attribute_groups)}")

    for records, label in [(category_nodes, "category"), (attribute_nodes, "attribute")]:
        ids = [str(values(graph, n, OGE.sourceTaxonomyID)[0]) for n in records]
        require(len(ids) == len(set(ids)), f"Duplicate {label} taxonomy IDs detected")

    # Ensure source concepts are represented as individuals and not asserted
    # equivalent to external classes solely by matching labels.
    require(not list(graph.triples((None, OWL.sameAs, None))), "Unexpected owl:sameAs assertion")
    require(not list(graph.triples((None, OWL.equivalentClass, None))), "Unexpected owl:equivalentClass assertion")

    print(f"Parsed {len(graph)} RDF triples from {ONTOLOGY_PATH.relative_to(ROOT)}")
    print("PASS: one ontology node")
    print("PASS: 46 Fashionpedia category records (27 main + 19 part-related)")
    print("PASS: 294 Fashionpedia attribute records across 11 source supercategories")
    print("PASS: source labels, IDs, groups, levels, and provenance are present")
    print("PASS: no owl:sameAs or owl:equivalentClass mappings are asserted")
    print("NOTE: RDF/Turtle structural checks do not replace OWL 2 DL reasoner validation.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
