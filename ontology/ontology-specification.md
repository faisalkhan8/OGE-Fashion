# OGE-Fashion Ontology Specification

**Project:** OGE-Fashion — An Ontology-Guided Explainable Recommendation Framework for Personalised Fashion and Beauty Recommendations  
**Specification version:** 0.3  
**Ontology file:** `oge-fashion-v0.1.ttl`  
**Status:** Working draft; RDF/Turtle parser, source-manifest checks, HermiT consistency classification, and 12 synthetic SPARQL competency tests pass in GitHub Actions. Full source semantics review and recommendation evaluation remain pending.  
**Proposed ontology identifier:** `https://w3id.org/oge-fashion/ontology` (proposed only; not claimed to be registered or resolvable).

## 1. Purpose and research boundaries

The ontology models fashion and makeup catalogue entities, their descriptive attributes, user preferences, recommendation context, explicit compatibility assessments, ranked recommendation results, scoring components, evidence, and traceable explanations.

It is intended to support a comparative recommendation study:

1. content-based baseline;
2. ontology-only semantic matching;
3. machine-learning/content-ranking baseline without ontology-derived compatibility;
4. hybrid ranking combining model signals and ontology-derived information.

The ontology itself does not establish that a recommendation is relevant or that a compatibility relation is objectively true. Those claims require data, a declared annotation method, and evaluation.

No universal beauty or style rules are encoded. Face-shape descriptors are optional and user-confirmed; the ontology does not state that a face shape determines suitable clothing or makeup. Sensitive facial inference, attractiveness scoring, medical advice, and identity recognition are outside the initial scope.

## 2. Historical FYP versus later research extension

The original university FYP period is **7th and 8th semesters, November 2023–May 2024**. The expanded OGE-Fashion ontology and implementation work recorded in this repository in November 2026 are later research development. Do not backdate the 2026 model, source mappings, code, or experiments into the original academic period.

See [historical FYP timeline](../research/fyp-timeline.md).

## 3. Namespace and representation

- OGE: `https://w3id.org/oge-fashion/ontology#`
- RDF: `http://www.w3.org/1999/02/22-rdf-syntax-ns#`
- RDFS: `http://www.w3.org/2000/01/rdf-schema#`
- OWL: `http://www.w3.org/2002/07/owl#`
- XSD: `http://www.w3.org/2001/XMLSchema#`
- Dublin Core Terms: `http://purl.org/dc/terms/`

Target: OWL 2 DL, authored in Turtle and opened in Protégé. The actual profile and consistency must be verified with an OWL 2 DL-capable reasoner.

## 4. Reuse and source alignment

### Fashionpedia

Fashionpedia's official project describes an expert-built fashion ontology with 27 main apparel categories, 19 apparel parts, and 294 fine-grained attributes. Its official Terms of Use state that the ontology and annotations are under CC BY 4.0; the underlying images are separately governed by original image-provider terms and are not included in this repository's taxonomy mapping.

The source term manifest is preserved in:
- [46 category mappings](source-mappings/fashionpedia-categories.csv)
- [294 attribute mappings](source-mappings/fashionpedia-attributes.csv)
- [extraction and attribution notes](source-mappings/fashionpedia-taxonomy-mapping.md)

The OGE-Fashion model preserves the source distinction between categories and attributes. Source terms are represented as named individuals with their source-local ID, taxonomy ID, exact label, supercategory, source level, and source URL. The 27 main category entries and 19 part-related entries are typed into OGE-Fashion group classes. The 294 attribute values are typed under 11 OGE-Fashion classes that correspond to source-defined attribute supercategories.

The group-to-class mapping is a project modelling decision, not a claim of formal equivalence. No `owl:sameAs`, `owl:equivalentClass`, or `owl:equivalentProperty` axioms are asserted solely because labels look similar. Source supercategory strings are retained as data; they are not silently converted into OWL subclass axioms.

### SERVIVE Fashion Ontology / style advice

Vogiatzis et al. (2012) describe an OWL-based garment-advice framework that combines a fashion ontology and expert rules with user-interaction/purchase-pattern information. This is important prior art. It means OGE-Fashion must not claim to invent ontology-based fashion recommendation or a general combination of expert knowledge and recommendation signals.

Reference: Vogiatzis, D., Pierrakos, D., Paliouras, G., Jenkyn-Jones, S., and Possen, B.J.H.H.A. (2012). “Expert and community based style advice.” *Expert Systems with Applications*, 39(12), 10647–10655. https://doi.org/10.1016/j.eswa.2012.02.178.

The prior work informs modelling questions, but this repository does not assume that its original ontology file, software, or data can be reused.

## 5. Class model

### Core recommendation and catalogue concepts
- `RecommendationEntity`: a candidate item or entity.
- `FashionItem`: fashion catalogue entity; includes `Garment`, `Outfit`, `Footwear`, and `Accessory`.
- `MakeupItem`: makeup catalogue entity; includes `MakeupProduct` and `MakeupLook`.
- `FaceMakeup`, `EyeMakeup`, and `LipMakeup`: product categories.
- `Attribute`: descriptive value concept.
- `Category`: classification concept kept distinct from descriptive attributes.
- `FashionCategory`: Fashionpedia-aligned category layer.
- `FashionpediaAttributeValue`: source-aligned attribute-value layer.

### Fashionpedia-aligned attribute groups
- `GarmentNicknameAttribute`
- `GarmentSilhouetteAttribute`
- `WaistlineAttribute`
- `GarmentLengthAttribute`
- `NecklineTypeAttribute`
- `OpeningTypeAttribute`
- `NonTextileMaterialTypeAttribute`
- `LeatherAttribute`
- `TextileFinishingTechniqueAttribute`
- `TextilePatternAttribute`
- `AnimalPatternAttribute`

### User, context, and preference concepts
- `UserProfile`, `ProfileAssertion`, and `Preference`.
- `Context`, `Occasion`, and `BudgetConstraint`.
- Optional `FaceAttribute` and `FaceShape`, with the values Oval, Diamond and Square retained from the earlier project concept.

A catalogue attribute is a statement about an item. A profile assertion is a user-specific statement and carries its own confirmation/origin information. A preference is a user's positive or negative selection. Do not conflate these records.

### Recommendation, compatibility and explanation concepts
- `Recommendation`: a request/result set for one profile and context.
- `RecommendationResult`: a single ranked candidate in a recommendation.
- `CompatibilityAssessment`: a reified relation between two items, with method, context, optional score, and evidence.
- `Explanation`: a traceable explanation linked to a particular result.
- `Evidence`: a source record, curated annotation, rule, or model output.
- `ScoringComponent`: one contribution to a recommendation score, with subclasses for learned-model and ontology-reasoning components.

## 6. Important object properties

| Property | Domain → Range | Purpose |
|---|---|---|
| `hasAttribute` | RecommendationEntity → Attribute | Item attribute |
| `hasCategory` | RecommendationEntity → Category | Item category |
| `hasFashionpediaCategory` | RecommendationEntity → FashionCategory | Source-aligned category |
| `hasFashionpediaAttribute` | RecommendationEntity → FashionpediaAttributeValue | Source-aligned attribute |
| `hasColour`, `hasStyle`, `hasMaterial`, `hasPattern`, `hasFit` | RecommendationEntity/FashionItem → corresponding attribute | Descriptive item characteristics |
| `hasFinish`, `hasApplicationStyle` | MakeupItem/MakeupProduct → makeup attribute | Makeup characteristics |
| `hasPreference` | UserProfile → Preference | Explicit preference |
| `hasProfileAssertion` | UserProfile → ProfileAssertion | User-specific attribute statement |
| `assertionAbout`, `assertionValue` | ProfileAssertion → Attribute | What an assertion describes and its value |
| `hasContext`, `hasOccasion` | UserProfile → Context/Occasion | User-selected context |
| `hasBudgetConstraint` | UserProfile → BudgetConstraint | Budget limit |
| `hasCompatibilityAssessment` | RecommendationEntity → CompatibilityAssessment | Item-linked assessment |
| `assessesItemA`, `assessesItemB` | CompatibilityAssessment → RecommendationEntity | The assessed pair |
| `assessmentEvidence` | CompatibilityAssessment → Evidence | Support for compatibility |
| `forProfile`, `forContext` | Recommendation → UserProfile/Context | Recommendation request context |
| `hasResult`, `resultItem` | Recommendation → RecommendationResult → RecommendationEntity | Ranked result |
| `hasRequiredAttribute` | Recommendation → Attribute | Attribute needed by the request |
| `hasResultExplanation` | RecommendationResult → Explanation | Explanation for a ranked result |
| `explanationPreference`, `explanationAttribute` | Explanation → Preference/Attribute | Preference and item attribute used |
| `explanationCompatibilityAssessment` | Explanation → CompatibilityAssessment | Compatibility evidence path |
| `explanationScoringComponent` | Explanation → ScoringComponent | Model or ontology contribution |
| `supportedBy` | Explanation → Evidence | Supporting source/record |

The direct `compatibleWith` property is not assumed to be symmetric or transitive. Context-sensitive relations should use `CompatibilityAssessment` so the pair, method, context, score and evidence can be inspected.

## 7. Important datatype properties

- Item and preference data: `priceAmount`, `currencyCode`, `preferencePolarity`, `preferenceWeight`, `preferenceDomain`, `isHardConstraint`.
- Profile assertion: `isUserConfirmed`, `assertionOrigin`.
- Compatibility: `compatibilityScore`, `methodName`, `methodVersion`.
- Result/scoring: `rankPosition`, `resultScore`, `componentName`, `componentVersion`, `scoreValue`.
- Explanation: `explanationStatus`, `explanationMessage`.
- Source provenance: `sourceLocalID`, `sourceTaxonomyID`, `sourceSupercategory`, `sourceTaxonomyLevel`, `sourceDataset`.

Controlled values are application-level validation constraints for now. SHACL shapes should be added when the allowed vocabularies and requirements are finalised.

## 8. Scoring model (conceptual only)

A candidate scoring design is:

`score(u,i,c) = w_m M(u,i,c) + w_o O(u,i,c) + w_p P(u,i,c) + w_c C(u,i,c)`

where M is a model/content signal, O an ontology-derived signal, P preference alignment, and C context/constraint fit. This is not a committed final algorithm. The weights, normalisation, calibration and aggregation must be justified and tuned on training/validation data only. A hard user exclusion is a filter, not a soft score bonus.

## 9. Modelling constraints

1. Separate catalogue facts, profile assertions, explicit preferences, learned predictions, and compatibility assessments.
2. Missing values are unknown; absence of an attribute is not proof of incompatibility.
3. Store price and currency separately.
4. Compatibility may be directional, subjective, method-dependent, and context-specific.
5. Curated/annotated compatibility must retain provenance and method details.
6. Never make universal suitability rules based on face shape, body type, skin tone, gender or other personal traits.
7. Users can correct profile assertions and edit preferences/exclusions.
8. Do not infer sensitive traits from images; image analysis is optional later work and requires consent, safeguards and ethics review.
9. Keep transactional user data in the application database; OWL represents semantic concepts and relationships rather than the full transaction store.
10. Dataset permissions, provenance, attribution and third-party image rights must be checked separately.

## 10. Competency questions and validation

The 20 competency questions are listed in [competency-questions.md](competency-questions.md). Twelve SPARQL query templates currently cover representative preference, constraint, context, category, attribute, missing-value, compatibility, evidence, explanation, model-score and insufficient-evidence cases. A synthetic fixture is used for software tests only.

- [SPARQL query templates](queries/competency-questions.rq)
- [Synthetic competency fixture](../tests/fixtures/competency-example.ttl)
- [SPARQL test runner](../scripts/test_competency_queries.py)
- [RDF/source-integrity validator](../scripts/validate_ontology.py)

RDF/Turtle parsing, deterministic structure checks, OWL reasoning, and query-level competency tests are separate validation layers. On 2026-11-15, GitHub Actions parsed 3,237 RDF triples; verified the 46 category and 294 attribute source records with provenance; ran Owlready2 0.51 using HermiT against 59 OWL classes with no ontology inconsistency and no named class equivalent to owl:Nothing; and passed 12/12 synthetic SPARQL tests. The HermiT runner is [scripts/reason_ontology.py](../scripts/reason_ontology.py). Its CI setup uses Java 17 and Owlready2 0.51. These checks establish logical consistency for the current asserted model and query behaviour on the supplied synthetic fixtures. They do not establish that the source mappings are semantically perfect, that compatibility judgements are factually correct, or that recommendations are relevant. No recommendation-quality or human-evaluation result is claimed.

## 11. Open decisions

- Which authoritative vocabulary should supply makeup product categories, finishes, colours and application concepts?
- Which OGE-Fashion properties should be object properties versus datatype properties for real catalogue data?
- Should a formal SKOS alignment layer be introduced after exact source-term review?
- Which SHACL shapes and controlled-value lists are necessary?
- What is the defensible source/annotation protocol for compatibility assessments?
- What eligible preference/relevance labels can support offline recommendation evaluation?
- What human-evaluation design and ethics approval are required for explanation usefulness?
