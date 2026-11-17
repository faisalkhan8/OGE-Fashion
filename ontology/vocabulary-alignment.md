# Preliminary vocabulary alignment for OGE-Fashion

**Status:** Concept-level alignment draft; exact source identifiers and term-by-term mappings remain to be extracted and reviewed.

## Why alignment is required

OGE-Fashion should not recreate an apparel taxonomy from scratch. The fashion branch will first align with existing published vocabularies, while the makeup and shared user/context branches will be added only where the project competency questions require them.

Two important prior-work sources are:

1. **Fashionpedia (ECCV 2020).** Its expert-built fashion ontology distinguishes 27 main apparel categories, 19 apparel parts, and 294 fine-grained attributes organised into nine super-categories. The project describes a distinction between categories and attributes and provides mappings to categories in other fashion segmentation datasets.
   - Project page: https://fashionpedia.github.io/home/index.html
   - Paper: https://doi.org/10.1007/978-3-030-58517-4_26
   - Official terms: https://fashionpedia.github.io/home/data_license.html
2. **Vogiatzis et al. (2012), “Expert and community based style advice.”** This work describes a garment-recommendation framework using an OWL fashion ontology covering garments, materials, colours, body types, facial features, social occasions, and their relationships, combined with expert rules and community/purchase-behaviour signals.
   - DOI: https://doi.org/10.1016/j.eswa.2012.02.178
   - Author-hosted paper: https://users.iit.demokritos.gr/~paliourg/old/papers/ESWA2012.pdf

## Initial alignment table

| Source concept/group | Proposed OGE-Fashion concept | Preliminary mapping relation | Rationale and implementation note |
|---|---|---|---|
| Fashionpedia main apparel categories | `FashionItem`, `Garment`, and a project-specific `Category` vocabulary | Broader/narrower mapping to be resolved per source term | Keep the source category hierarchy; do not assert that every source category is exactly equivalent to the broad OGE class `Garment`. |
| Fashionpedia apparel parts | `GarmentPart` and `hasPart` | Related; candidate narrower terms | Preserve parts as distinct from whole garments. Extract the source's exact part labels/IDs before creating individuals or subclasses. |
| Fashionpedia fine-grained attributes | `Attribute` and suitable attribute subclasses such as `Colour`, `Material`, `Pattern`, and `Fit` | Related; exact mapping per attribute pending | Do not map all 294 attributes to one generic property. Retain source category/attribute distinctions and document ambiguous terms. |
| Fashionpedia category-versus-attribute distinction | OGE-Fashion distinction between item category and descriptive attributes | Conceptual alignment | This is a modelling pattern to preserve, not a reason to import the entire dataset or image collection. |
| SERVIVE generic garments | `Garment` / `FashionItem` | Close conceptual alignment; term-level review pending | Use the paper's modelling pattern as prior art; do not assume its ontology file or code is reusable. |
| SERVIVE materials and colours | `Material` and `Colour` | Close conceptual alignment; exact source URIs not established | Reuse the concepts, but define OGE-Fashion identifiers independently until the source ontology and its terms are inspected. |
| SERVIVE body types and facial features | Optional `FaceAttribute` / `FaceShape` | Related; not equivalent by default | Retain as optional, user-confirmed descriptors only. Do not encode stereotypes or universal rules that a face/body type determines suitable garments. |
| SERVIVE social occasions | `Occasion` and `Context` | Close conceptual alignment | Occasion should be represented as contextual information that can affect a recommendation, not as an absolute style rule. |
| SERVIVE expert style rules | `CompatibilityAssessment`, `Evidence`, and `Explanation` | Related modelling pattern | Store each compatibility assertion with source, context, and method. Do not copy unsupported expert stereotypes as universal axioms. |
| SERVIVE purchase/community signals | Model features outside the core ontology; optionally trace them through `Evidence` | Deliberately not mapped to a static ontology class | Purchase/community signals are learned or observed recommender inputs, not timeless semantic facts about an item or user. |
| Makeup catalogue categories and product attributes | `MakeupProduct`, `FaceMakeup`, `EyeMakeup`, `LipMakeup`, `MakeupFinish`, `ApplicationStyle` | Project-specific extension; source mapping pending | Validate source category labels and their meaning before converting data tags into ontology classes. |
| Shared user preferences and constraints | `UserProfile`, `Preference`, `Context`, and `BudgetConstraint` | Project-specific integration | Keep explicit user preferences separate from catalogue facts, model predictions, and inferred attributes. |

## Source identifiers and mapping limits

This is a concept-level map, not a completed formal alignment. The sources above establish the major concept groups, but the source-specific term identifiers and full label lists have not yet been captured in this document. Therefore:

- Do not use `owl:equivalentClass` or `owl:equivalentProperty` based only on matching English labels.
- Do not create Fashionpedia-derived subclasses or individuals until the source labels, identifiers, hierarchy, and attribution requirements are recorded.
- Record each final mapping as exact, broader, narrower, related, or intentionally unmapped, with a rationale.
- Keep Fashionpedia ontology/annotation attribution separate from image copyright. Fashionpedia states that its ontology and annotations are CC BY 4.0, while it does not own the underlying images; image use is governed by the original image-source terms.
- Treat the SERVIVE paper as prior art. Do not assume the published paper grants permission to reuse an ontology file, code, or dataset.

## Decisions for ontology v0.1

1. Establish only the high-level shared classes and relationships needed for the competency questions.
2. Keep fashion and makeup modules separate under a shared recommendation/entity layer.
3. Preserve explicit provenance and evidence for compatibility assessments.
4. Include optional face-shape descriptors for continuity with the earlier FYP concept, but no deterministic face-shape-to-fashion/makeup rules.
5. Defer detailed fashion category taxonomies until the term-level alignment is complete.
