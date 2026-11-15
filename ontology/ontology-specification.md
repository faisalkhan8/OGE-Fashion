# OGE-Fashion Ontology Specification
**Proposed ontology identifier:** https://w3id.org/oge-fashion/ontology  
**Version:** 0.1 — conceptual proposal, not yet validated  
**Target representation:** OWL 2 DL, serialised as Turtle or RDF/XML.

## 1. Intent
Represent fashion and makeup catalogue entities, descriptive attributes, user preferences, contexts, constraints, explicit compatibility relations, and traceable explanations. Treat existing fashion ontologies (notably Fashionpedia and SERVIVE Fashion Ontology) as prior art and alignment candidates; do not duplicate their taxonomies without a documented need.

The ontology must not encode universal beauty rules. Compatibility relations must be traceable to a declared source, annotation protocol, or user preference signal, with provenance and confidence where applicable.

## 2. Namespace proposal
- OGE: `https://w3id.org/oge-fashion/ontology#`
- RDF: `http://www.w3.org/1999/02/22-rdf-syntax-ns#`
- RDFS: `http://www.w3.org/2000/01/rdf-schema#`
- OWL: `http://www.w3.org/2002/07/owl#`
- XSD: `http://www.w3.org/2001/XMLSchema#`
- Optional PROV-O: `http://www.w3.org/ns/prov#`

The w3id URI is proposed; it is not claimed to be registered or resolvable.

## 3. Reuse and alignment strategy
Before adding fashion classes, compare terms, hierarchy, labels, relationships, and competency coverage in Fashionpedia and the published SERVIVE/style-advice work. Keep an explicit mapping table containing source term, source URI/identifier, proposed OGE term, mapping relation, rationale, and licence/attribution note. Reuse or adapt only material whose terms allow it. Document non-equivalences; do not assert exact equivalence merely because labels look similar. The makeup vocabulary should likewise be aligned to identified authoritative or otherwise appropriate terminology sources once selected.

The project-specific contribution, if supported by evidence, should be in the cross-domain integration, user/context semantics, traceable evidence representation, or evaluation—not in claiming to originate a fashion taxonomy.

## 4. Upper-level classes
| Class | Description |
|---|---|
| `RecommendationEntity` | Entity eligible for recommendation |
| `FashionItem` | Fashion catalogue entity |
| `MakeupItem` | Makeup catalogue entity |
| `UserProfile` | User-controlled preference profile |
| `Preference` | Positive, negative, or neutral preference statement |
| `Context` | Occasion or other recommendation context |
| `Attribute` | Descriptive feature/value concept |
| `CompatibilityRelation` | Documented relation between entities |
| `Recommendation` | Ranked output for a profile/context |
| `Explanation` | Evidence-grounded explanation record |
| `Evidence` | Provenance or supporting observation/rule/model output |

### Fashion subdomain
`Garment`, `Outfit`, `Footwear`, `Accessory`, `ClothingCategory`, `Material`, `Pattern`, `Fit`, `GarmentStyle`.

### Makeup subdomain
`FaceMakeup`, `EyeMakeup`, `LipMakeup`, `MakeupLook`, `MakeupProductCategory`, `MakeupFinish`, `ApplicationStyle`.

### Shared concepts
`Colour`, `ColourFamily`, `Style`, `Occasion`, `BudgetRange`, `Brand` (only where data rights support its use), and optional `FaceAttribute` (user-confirmed or consent-derived; not required for the core ontology).

## 5. Candidate object properties
| Property | Domain → Range | Meaning |
|---|---|---|
| `hasAttribute` | RecommendationEntity → Attribute | Documented attribute |
| `hasColour` | RecommendationEntity → Colour | Colour attribute |
| `hasStyle` | RecommendationEntity → Style | Style association |
| `hasCategory` | RecommendationEntity → Category | Catalogue category |
| `hasMaterial` | FashionItem → Material | Material description |
| `hasPattern` | FashionItem → Pattern | Pattern description |
| `hasFinish` | MakeupItem → MakeupFinish | Makeup finish |
| `hasPreference` | UserProfile → Preference | User-selected preference |
| `hasContext` | UserProfile → Context | User-selected occasion/context |
| `compatibleWith` | RecommendationEntity → RecommendationEntity | Explicit compatibility assertion |
| `recommendedFor` | RecommendationEntity → UserProfile | Optional persisted recommendation relation |
| `explains` | Explanation → Recommendation | Explanation supports recommendation |
| `supportedBy` | Explanation → Evidence | Link to provenance/evidence |
| `derivedFrom` | Evidence → Evidence | Provenance relation |

Review domain/range axioms to avoid unintended type inferences. Do not make `compatibleWith` symmetric or transitive unless its semantics and evidence justify that choice.

## 6. Candidate data properties
| Property | Datatype | Notes |
|---|---|---|
| `label` | xsd:string | Human-readable name |
| `description` | xsd:string | Description |
| `priceAmount` | xsd:decimal | Price; currency stored separately |
| `currencyCode` | xsd:string | ISO currency code where known |
| `preferencePolarity` | xsd:string | Controlled vocabulary: positive/negative/neutral |
| `preferenceWeight` | xsd:decimal | User-selected or learned weight; define range |
| `confidenceScore` | xsd:decimal | Method-specific confidence, not certainty |
| `compatibilityScore` | xsd:decimal | Score from a defined method, not an intrinsic truth |
| `sourceIdentifier` | xsd:string | External provenance identifier |
| `isUserConfirmed` | xsd:boolean | User confirmation flag |

Associate scores with scoring method/version and context. They are not timeless facts about a person's appearance.

## 7. Modelling constraints
1. Separate catalogue facts from preferences and predictions.
2. Use explicit classes/controlled vocabularies for important categorical fields.
3. Missing values are unknown, not negative preferences.
4. Store price and currency separately.
5. Compatibility may be directional and context-dependent.
6. Do not hard-code rules asserting that face shape determines suitable garments or makeup.
7. Users can edit profile attributes, preferences, and exclusions.
8. Curated/annotated compatibility relations need provenance.
9. Sensitive attributes are outside initial scope.
10. Keep transactional user data in an application database; the ontology models semantic concepts/relations, not the full transactional store.

## 8. Competency questions
See [competency-questions.md](competency-questions.md). Test the ontology with synthetic individuals and reproducible queries.

## 9. Reasoning and validation
- Author and inspect with Protégé.
- Parse RDF with RDFLib.
- Use a compatible OWL 2 reasoner (e.g., HermiT in a supported runtime) for consistency/classification.
- Test SPARQL against synthetic examples.
- Add positive, negative, and unknown cases for domain/range and compatibility assumptions.
- Record reasoner version, ontology commit, outputs, and limitations.

## 10. Proposed modules
- `core`: RecommendationEntity, Attribute, Colour, Style, Context, UserProfile, Preference.
- `fashion`: Garment, Outfit, Footwear, Accessory, Material, Pattern, Fit.
- `makeup`: FaceMakeup, EyeMakeup, LipMakeup, MakeupLook, MakeupFinish.
- `recommendation`: Recommendation, Explanation, score records.
- `provenance`: Evidence and source metadata.

## 11. Open design questions
- Which upper ontology, if any, improves interoperability without unnecessary complexity?
- Should outfit compatibility be a direct relation, a reified assessment, or both?
- How should preference strength and uncertainty be represented?
- What belongs in OWL axioms versus SHACL constraints or application validation?
- Which colour vocabulary is appropriate and maintainable?
- What evidence supports each compatibility rule, and how are subjective rules versioned?

Resolve these through requirements, literature, and tests rather than assumptions.
