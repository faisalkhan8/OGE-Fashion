from __future__ import annotations

from pathlib import Path
import sys

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
DATA_FILES = [
    ROOT / "ontology" / "oge-fashion-v0.1.ttl",
    ROOT / "tests" / "fixtures" / "competency-example.ttl",
]
SHAPES_FILE = ROOT / "ontology" / "shapes" / "oge-fashion-shapes.ttl"


def load_graph(paths: list[Path]) -> Graph:
    graph = Graph()
    for path in paths:
        graph.parse(path, format="turtle")
    return graph


def main() -> int:
    data_graph = load_graph(DATA_FILES)
    shapes_graph = load_graph([SHAPES_FILE])
    conforms, report_graph, report_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        meta_shacl=True,
        advanced=True,
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
    )
    print(f"Validated {len(data_graph)} RDF data triples against {len(shapes_graph)} SHACL shape triples")
    print(report_text)
    if not conforms:
        print("FAIL: SHACL data validation did not conform", file=sys.stderr)
        return 1
    print("PASS: synthetic OGE-Fashion profile, preference, budget, compatibility, recommendation, explanation, and source provenance records conform to SHACL")
    print("NOTE: the current fixture is synthetic. SHACL conformance is a data-structure check, not a recommendation-quality result.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: SHACL validation could not complete: {exc}", file=sys.stderr)
        raise
