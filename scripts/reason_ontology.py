from __future__ import annotations

from pathlib import Path
import sys
import tempfile

from rdflib import Graph
from owlready2 import (
    Nothing,
    OwlReadyInconsistentOntologyError,
    get_ontology,
    sync_reasoner,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ontology" / "oge-fashion-v0.1.ttl"


def main() -> int:
    # Owlready2/HermiT is used for OWL-level reasoning. Convert the committed
    # Turtle document to RDF/XML through RDFLib first, so the reasoner reads
    # exactly the same asserted graph that the structural validator parses.
    graph = Graph()
    graph.parse(SOURCE, format="turtle")

    with tempfile.TemporaryDirectory(prefix="oge-fashion-reasoner-") as temp_dir:
        rdfxml_path = Path(temp_dir) / "oge-fashion.owl"
        graph.serialize(destination=str(rdfxml_path), format="xml")

        ontology = get_ontology(rdfxml_path.resolve().as_uri()).load()
        asserted_classes = list(ontology.classes())

        print(f"Loaded ontology for HermiT reasoning: {len(asserted_classes)} classes")
        try:
            with ontology:
                sync_reasoner([ontology], debug=1)
        except OwlReadyInconsistentOntologyError as exc:
            print(f"FAIL: ontology is inconsistent: {exc}", file=sys.stderr)
            return 1

        unsatisfiable = [
            cls for cls in ontology.classes()
            if Nothing in cls.equivalent_to
        ]
        if unsatisfiable:
            labels = sorted(str(cls.iri) for cls in unsatisfiable)
            print("FAIL: unsatisfiable classes detected:", file=sys.stderr)
            for iri in labels:
                print(f"  - {iri}", file=sys.stderr)
            return 1

        print("PASS: HermiT completed without reporting ontology inconsistency")
        print("PASS: no named OGE-Fashion classes are equivalent to owl:Nothing")
        print("NOTE: logical consistency does not establish that modelling choices are factually correct or that recommendations are useful.")
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: reasoner validation could not complete: {exc}", file=sys.stderr)
        raise
