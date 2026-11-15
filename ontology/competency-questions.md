# Ontology Competency Questions
These questions define the intended information needs of OGE-Fashion. They are acceptance targets, not claims that the current draft can already answer them.

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

## Validation scenarios
- **Positive:** user selects a colour and occasion; an item has matching documented attributes.
- **Negative:** user excludes a colour; an item with that colour is removed when the exclusion is a hard constraint.
- **Unknown:** item material is unrecorded; the system does not claim it is compatible or incompatible.
- **Traceability:** an explanation resolves to a relation ID, evidence record, or scoring component.
- **User correction:** an edited preference changes subsequent query results.

## Acceptance
A question is covered only when required classes/properties exist, a reproducible fixture contains the facts, a query/reasoner test returns the expected result, negative/unknown cases are tested where appropriate, and expected/actual outputs are recorded.
