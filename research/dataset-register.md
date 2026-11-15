# Dataset and Data-Source Register
**Version:** 0.1 — candidates only; not an approval list.

## Acceptance checklist
A source may be used only after its identity, access conditions, licence, permitted purposes, redistribution limits, attribution, provenance, and suitability for the planned research are recorded. Public download availability does not imply commercial reuse rights.

## Candidate register
| Source | Potential role | What it appears to offer | Risks / limitations | Status |
|---|---|---|---|---|
| Fashionpedia | Clothing object/attribute representation | Project describes 48,825 images, 46 apparel object categories, and 294 fine-grained attributes | Confirm exact terms, access process, version, redistribution permissions; does not directly provide personal preferences or makeup labels | Candidate; due diligence required |
| DeepFashion | Clothing attributes, retrieval, landmarks and related tasks | Research dataset and fashion-understanding benchmarks | Project page states non-commercial research restrictions; do not use images in a commercial product without separate permission | Candidate; terms must be reviewed |
| Polyvore outfit compatibility data | Outfit composition/compatibility research | Potentially useful compatibility labels | Current access, provenance, and licence not verified | Unverified candidate |
| Makeup datasets | Makeup categories/styles/attributes | No specific source approved yet | Assess definitions, rights, demographics, consent, licence | Open research task |
| Curated catalogue metadata | Ontology development and controlled prototype | Can represent product attributes from documented sources/original annotation | Requires rights and a documented annotation protocol; distinguish facts from subjective judgements | Possible fallback |

## Sources to inspect
- Fashionpedia: https://fashionpedia.github.io/home/index.html
- DeepFashion: https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html

## Required record per source
Record dataset name, official URL, owner/publisher, version/access date, citation, full licence and terms, allowed research/commercial/modification/redistribution uses, attribution, personal-data/consent issues, fields/label definitions, known bias, intended role, and final decision (approved, restricted, rejected, or pending).

## Data segregation
- Keep raw/restricted data outside the public Git repository.
- Commit schemas, data dictionaries, source manifests, synthetic examples, and permitted metadata only.
- Do not publish user/face images, scraped personal data, or dataset assets without explicit rights.
- Keep research-only data separate from material intended for a public/commercial deployment.

## Next action
Complete licence due diligence for Fashionpedia and DeepFashion, then investigate makeup data candidates. Do not begin training against unverified dataset access.
