# Ontology Competency Questions

These 20 questions define the intended information needs of OGE-Fashion. They are acceptance targets; a question is not considered fully covered merely because it has a prose description.

## User profile and preferences

1. Which fashion preferences has a user explicitly selected?
2. Which makeup preferences has a user explicitly selected?
3. Which colours or styles has a user excluded?
4. Which budget and occasion constraints apply to a request?
5. Which attributes are user-confirmed, inferred, or missing?

## Fashion

6. Which garments belong to a requested category?
7. Which fashion items have a specified colour, material, pattern, fit, or style?
8. Which outfit components have a documented compatibility relation?
9. What evidence or rule supports that relation?
10. Which items violate a hard user constraint?

## Makeup

11. Which makeup items belong to face, eye, or lip categories?
12. Which makeup items have a specified colour, finish, or application style?
13. Which makeup items match explicit user preferences and exclusions?
14. What evidence supports a makeup compatibility relation?
15. Which required attributes are missing from a candidate item?

## Cross-domain

16. Which fashion and makeup items match a selected occasion and style preference?
17. Which shared colour/style concepts occur across a fashion item and makeup item?
18. Can an explanation identify the user preference, item attribute, and ontology relation supporting a recommendation?
19. Which recommendation component depends on a learned model score rather than an ontology assertion?
20. Can the system return an insufficient-evidence explanation when a relation is absent?

## Executable coverage currently added

The following SPARQL templates and synthetic tests are in the repository:

| Query | Coverage | Current implementation |
|---|---|---|
| CQ01 | Fashion preferences | Explicit domain and positive preference lookup |
| CQ02 | Makeup preferences | Explicit domain and positive preference lookup |
| CQ03 | Hard exclusions | Find candidate items matching a hard negative preference |
| CQ04 | Budget and occasion | Retrieve selected context and budget constraint |
| CQ05 | Profile assertion origin | Distinguish user-confirmed and model-inferred assertions |
| CQ06 | Fashion categories | Query source-aligned category individuals |
| CQ07 | Makeup attributes | Query makeup category, colour, finish and style |
| CQ08 | Missing required attribute | Find garment candidates that lack a required material value |
| CQ09 | Compatibility with evidence | Retrieve an assessment and its evidence record |
| CQ10 | Explanation traceability | Link a ranked result to preference, attribute, assessment and evidence |
| CQ11 | Learned model contribution | Identify and retrieve a learned-model score component |
| CQ12 | Insufficient evidence | Find an explanation marked insufficient where assessment evidence is absent |

The executable cases use only [synthetic fixture data](../tests/fixtures/competency-example.ttl). They do not provide user-preference labels, human relevance judgements, evidence that an item combination is objectively compatible, or a performance evaluation. CQ8 tests absence of a required value; it does not classify the item as incompatible.

### Still requiring additional dedicated tests

- Full attribute coverage for every fashion attribute group and every makeup property.
- Makeup exclusion and preference-based filtering under multiple competing constraints.
- Outfit composition and multi-item compatibility.
- Constraint combinations involving budget, occasion, and item exclusions.
- User correction/update behaviour across repeated recommendation requests.
- Recommendation coverage, diversity, latency and ranking metrics.
- Human evaluation of explanation usefulness after ethics approval.

## Validation scenarios

- **Positive:** a user selects a colour and occasion; an item has matching documented attributes.
- **Negative:** a user excludes a colour; an item with that colour is removed when the exclusion is a hard constraint.
- **Unknown:** an item material is unrecorded; the system does not claim it is compatible or incompatible.
- **Traceability:** an explanation resolves to a preference, attribute, relation/assessment, evidence record or score component.
- **User correction:** an edited preference changes subsequent query results.

## Acceptance

A question is covered only when its required classes/properties exist, a reproducible fixture contains the facts, a query/reasoner test returns the expected result, negative/unknown cases are tested where appropriate, and expected/actual outputs are recorded.
