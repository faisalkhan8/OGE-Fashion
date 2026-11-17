from __future__ import annotations

"""Synthetic, deterministic comparison of attribute ranking and SPARQL filtering.

All profiles and catalogue entries are constructed fixtures. This benchmark is
not evidence about real users, skin-tone suitability, or generalisation.
"""

import argparse
import json
import math
import random
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "oge-fashion-v0.1.ttl"
OUT = ROOT / "results"
OGE = Namespace("https://w3id.org/oge-fashion/ontology#")
BASE = "https://w3id.org/oge-fashion/benchmark/"
SEED, K = 20261117, 3
PALETTES = {"warm": "#D58A45", "cool": "#6B83B8", "neutral": "#9A806B"}
ITEMS = [
    ("item01", "Warm office blazer", "#B87333", "office", "formal", "classic"),
    ("item02", "Cool office blazer", "#5577AA", "office", "formal", "classic"),
    ("item03", "Neutral office blazer", "#8A7968", "office", "formal", "minimal"),
    ("item04", "Warm casual jacket", "#C17A3A", "casual", "casual", "relaxed"),
    ("item05", "Cool casual jacket", "#607DA8", "casual", "casual", "relaxed"),
    ("item06", "Neutral casual jacket", "#918071", "casual", "casual", "minimal"),
    ("item07", "Warm evening dress", "#B96535", "evening", "formal", "classic"),
    ("item08", "Cool evening dress", "#536A9B", "evening", "formal", "classic"),
    ("item09", "Neutral evening dress", "#927A6B", "evening", "formal", "minimal"),
    ("item10", "Warm smart-casual shirt", "#C18A50", "office", "smart_casual", "minimal"),
    ("item11", "Cool smart-casual shirt", "#7189B2", "office", "smart_casual", "minimal"),
    ("item12", "Neutral smart-casual shirt", "#9C8B7A", "office", "smart_casual", "classic"),
    ("item13", "Warm weekend outfit", "#C78A4B", "weekend", "casual", "relaxed"),
    ("item14", "Cool weekend outfit", "#7184B2", "weekend", "casual", "relaxed"),
    ("item15", "Neutral weekend outfit", "#A08C7A", "weekend", "casual", "minimal"),
    ("item16", "Warm formal suit", "#A96B38", "office", "formal", "minimal"),
    ("item17", "Cool formal suit", "#536B91", "office", "formal", "minimal"),
    ("item18", "Neutral formal suit", "#8C7B70", "office", "formal", "classic"),
]


def colour_distance(a: str, b: str) -> float:
    def channels(value: str):
        value = value.removeprefix("#")
        if len(value) != 6:
            raise ValueError(f"Invalid HEX colour: {value}")
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(channels(a), channels(b))))


def profiles():
    values = []
    for i in range(24):
        item = ITEMS[i % len(ITEMS)]
        tone = ("warm", "cool", "neutral")[i % 3]
        values.append({
            "profile_id": f"synthetic-{i:02d}",
            "skin_undertone": tone,  # synthetic descriptor, not a measurement
            "reference_colour": PALETTES[tone],
            "occasion": item[3],
            "dress_code": item[4],
            "style": item[5],
        })
    return values


def graph_with_fixture():
    graph = Graph()
    graph.parse(ONTOLOGY, format="turtle")
    # These generated assertions are in-memory only; source ontology is unchanged.
    for iid, label, colour, occasion, dress, style in ITEMS:
        item = URIRef(BASE + iid)
        graph.add((item, RDF.type, OGE.Garment))
        graph.add((item, OGE.label, Literal(label)))
        for prop, value, cls in (
            (OGE.hasOccasion, occasion, OGE.Occasion),
            (OGE.hasStyle, dress, OGE.Style),
            (OGE.hasStyle, style, OGE.Style),
        ):
            concept = URIRef(BASE + str(prop).rsplit("#", 1)[-1] + "/" + value)
            graph.add((concept, RDF.type, cls))
            graph.add((concept, RDFS.label, Literal(value)))
            graph.add((item, prop, concept))
        shade = URIRef(BASE + "colour/" + colour.removeprefix("#"))
        graph.add((shade, RDF.type, OGE.Colour))
        graph.add((shade, OGE.label, Literal(colour)))
        graph.add((item, OGE.hasColour, shade))
    return graph


def allowed_by_sparql(graph, profile):
    query = f'''PREFIX oge: <{OGE}>
PREFIX rdfs: <{RDFS}>
SELECT DISTINCT ?item WHERE {{
  ?item a oge:Garment ;
        oge:hasOccasion ?occasion ;
        oge:hasStyle ?dressCode ;
        oge:hasStyle ?style .
  ?occasion rdfs:label "{profile["occasion"]}" .
  ?dressCode rdfs:label "{profile["dress_code"]}" .
  ?style rdfs:label "{profile["style"]}" .
}} ORDER BY ?item'''
    return {str(row.item).rsplit("/", 1)[-1] for row in graph.query(query)}


def score(item, profile):
    colour_fit = max(0.0, 1.0 - colour_distance(item[2], profile["reference_colour"]) / 441.673)
    return (0.55 * colour_fit + 0.20 * (item[3] == profile["occasion"])
            + 0.15 * (item[4] == profile["dress_code"]) + 0.10 * (item[5] == profile["style"]))


def relevant(item, profile):
    return (item[3] == profile["occasion"] and item[4] == profile["dress_code"]
            and item[5] == profile["style"]
            and colour_distance(item[2], profile["reference_colour"]) <= 155.0)


def baseline(profile):
    chosen = sorted(ITEMS, key=lambda x: (-score(x, profile), x[0]))[:K]
    return [{"item_id": x[0], "score": round(score(x, profile), 6), "trace": []} for x in chosen]


def ontology_rank(graph, profile):
    allowed = allowed_by_sparql(graph, profile)
    chosen = sorted((x for x in ITEMS if x[0] in allowed),
                    key=lambda x: (-score(x, profile), x[0]))[:K]
    output = []
    for x in chosen:
        output.append({
            "item_id": x[0], "score": round(score(x, profile), 6),
            "trace": [
                {"property": "oge:hasOccasion", "requested": profile["occasion"], "item_value": x[3], "status": "satisfied"},
                {"property": "oge:hasStyle (dress-code)", "requested": profile["dress_code"], "item_value": x[4], "status": "satisfied"},
                {"property": "oge:hasStyle (style)", "requested": profile["style"], "item_value": x[5], "status": "satisfied"},
                {"property": "oge:hasColour", "reference_colour": profile["reference_colour"],
                 "item_colour": x[2], "encoded_sRGB_euclidean_distance": round(colour_distance(x[2], profile["reference_colour"]), 3),
                 "status": "soft_ranking_signal"},
            ],
        })
    return output


def dcg(values):
    return sum(v / math.log2(i + 2) for i, v in enumerate(values))


def measure(rows, key):
    accum = {name: [] for name in ("p", "r", "ndcg", "constraints", "traces")}
    for row in rows:
        p, top = row["profile"], row[key][:K]
        relevant_ids = {x[0] for x in ITEMS if relevant(x, p)}
        hits = [int(rec["item_id"] in relevant_ids) for rec in top]
        accum["p"].append(sum(hits) / K)
        accum["r"].append(sum(hits) / len(relevant_ids) if relevant_ids else 0.0)
        ideal = [1] * min(K, len(relevant_ids)) + [0] * max(0, K - len(relevant_ids))
        accum["ndcg"].append(dcg(hits) / dcg(ideal) if dcg(ideal) else 0.0)
        selected = [next(x for x in ITEMS if x[0] == rec["item_id"]) for rec in top]
        accum["constraints"].append(sum(
            x[3] == p["occasion"] and x[4] == p["dress_code"] and x[5] == p["style"]
            for x in selected) / len(selected) if selected else 0.0)
        accum["traces"].append(sum(bool(rec["trace"]) for rec in top) / len(top) if top else 0.0)
    mean = lambda xs: round(sum(xs) / len(xs), 6) if xs else 0.0
    return {
        "precision_at_3": mean(accum["p"]), "recall_at_3": mean(accum["r"]),
        "ndcg_at_3": mean(accum["ndcg"]), "constraint_satisfaction_rate": mean(accum["constraints"]),
        "explanation_trace_coverage": mean(accum["traces"]),
    }


def run():
    all_profiles = profiles()
    shuffled = all_profiles[:]
    random.Random(SEED).shuffle(shuffled)
    test = shuffled[:len(shuffled) // 4]
    graph = graph_with_fixture()
    rows = [{"profile": p, "baseline": baseline(p), "ontology_guided": ontology_rank(graph, p)} for p in test]
    return {
        "experiment": "synthetic_baseline_vs_ontology_guided_v1",
        "seed": SEED, "k": K, "profile_count": len(all_profiles),
        "test_profile_count": len(test), "test_profile_ids": [r["profile"]["profile_id"] for r in rows],
        "catalogue_item_count": len(ITEMS), "data_status": "synthetic_constructed_benchmark",
        "ground_truth_definition": "Exact occasion, dress-code and style match plus encoded-sRGB Euclidean colour distance <= 155.",
        "conditions": {
            "A_baseline": "Weighted colour-distance and attribute score over all catalogue items; no hard filtering.",
            "B_ontology_guided": "SPARQL over committed OGE ontology plus in-memory synthetic RDF facts filters exact occasion, dress-code and style; remaining items use the same score and receive structured traces.",
        },
        "metrics": {"A_baseline": measure(rows, "baseline"), "B_ontology_guided": measure(rows, "ontology_guided")},
        "per_profile": [{
            "profile_id": r["profile"]["profile_id"], "profile": r["profile"],
            "baseline_top_k": r["baseline"], "ontology_guided_top_k": r["ontology_guided"],
        } for r in rows],
        "interpretation_boundary": (
            "Deterministic synthetic benchmark only. Labels are generated from the same constructed fields used by the constraints. "
            "Results demonstrate implementation behaviour on this fixture; they do not establish real-world recommendation quality, "
            "user preference, generalisation, causal benefit or statistical significance."
        ),
    }


def write_results(result):
    OUT.mkdir(exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    a, b = result["metrics"]["A_baseline"], result["metrics"]["B_ontology_guided"]
    specs = [
        ("Precision@3", "precision_at_3"), ("Recall@3", "recall_at_3"),
        ("NDCG@3", "ndcg_at_3"), ("Constraint satisfaction rate", "constraint_satisfaction_rate"),
        ("Explanation trace coverage", "explanation_trace_coverage"),
    ]
    lines = [
        "# Synthetic recommender benchmark — results", "",
        f"- Seed: {SEED}; K: {K}.",
        f"- Profiles: {result['profile_count']} generated; {result['test_profile_count']} held-out test profiles.",
        f"- Catalogue: {result['catalogue_item_count']} synthetic items.",
        "- Split: deterministic 75/25 shuffled split; both conditions use identical held-out profiles.",
        "- Relevance labels: exact occasion, dress-code and style match plus encoded-sRGB Euclidean colour distance <= 155.", "",
        "| Metric | A: non-ontology baseline | B: SPARQL/ontology-guided | B − A |", "|---|---:|---:|---:|",
    ]
    for label, field in specs:
        lines.append(f"| {label} | {a[field]:.4f} | {b[field]:.4f} | {b[field]-a[field]:+.4f} |")
    lines += [
        "", "## Interpretation", "",
        "Both conditions use the same colour/attribute score. A ranks the full catalogue. B applies SPARQL filters using OGE hasOccasion and hasStyle assertions, then ranks the surviving items and attaches structured property-level traces.",
        "",
        "Relevance labels are generated from the same synthetic fields used by the constraints. Differences are therefore implementation properties of this fixture, not independent evidence of improved recommendations for people. Trace coverage records trace presence, not human-perceived clarity or usefulness.",
        "", "## Limitations", "", result["interpretation_boundary"],
        "- Profiles, reference colours and catalogue are synthetic; the undertone field is not inferred from a person.",
        "- Colour distance is Euclidean distance in encoded sRGB, not CIEDE2000 or a validated skin-tone/foundation method.",
        "- SPARQL rules are benchmark constraints aligned with OGE properties. HermiT is not invoked for per-request inference.",
        "- No real users, observed preference labels, learned model, uncertainty intervals or statistical tests are involved.",
        "- Dress-code and style labels are illustrative, not universal fashion rules.",
        "", "Reproduce with: python experiments/evaluate_recommender.py (requires rdflib>=7.1,<8).", "",
    ]
    (OUT / "evaluation_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="print one ontology-guided explanation trace")
    args = parser.parse_args()
    result = run()
    write_results(result)
    if args.demo:
        sample = result["per_profile"][0]
        print(json.dumps({"profile_id": sample["profile_id"], "profile": sample["profile"],
                          "recommendations": sample["ontology_guided_top_k"]}, indent=2))
    else:
        print(json.dumps(result["metrics"], indent=2))
    print("Wrote results/metrics.json and results/evaluation_summary.md")


if __name__ == "__main__":
    main()
