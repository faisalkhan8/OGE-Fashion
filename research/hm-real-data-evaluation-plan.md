# Real-data evaluation plan: H&M Personalized Fashion Recommendations

**Prepared:** 2026-11-22  
**Status:** recommended candidate; not downloaded, accepted, or analysed yet  
**Purpose:** define a lawful and reproducible data path for evaluating OGE-Fashion beyond its existing synthetic fixture.

## 1. Why this dataset is the first candidate

The H&M Personalized Fashion Recommendations dataset is a closer match to OGE-Fashion's fashion recommender task than the current synthetic benchmark. The official Kaggle data page describes:
- customer purchase histories over time;
- `articles.csv` with article metadata;
- `customers.csv` with customer metadata;
- `transactions_train.csv` with customer, article, date, price, and sales-channel records;
- optional article images, which are not necessary for the first experiment.

The official data explorer reports 34.56 GB in total, so the initial experiment should use the CSV files only and avoid downloading the image archive unless a later experiment has a documented need and rights review.

Official source pages:
- Data description: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data
- Competition rules: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/rules

The competition rules state that data use is limited to non-commercial purposes, including academic research and education. They also prohibit transmitting, duplicating, publishing, redistributing, or otherwise making the competition data available to people who have not accepted the rules. This means:
- each researcher who accesses the data must register and accept the applicable rules;
- do not commit raw data, images, customer records, or derived row-level data to GitHub;
- do not place sample customer IDs or transaction records in public issues, notebooks, logs, papers, or supplementary files;
- publish only code and aggregate results after checking the current rules and the intended academic use;
- keep the private local data location outside Git and outside CI;
- re-check the rules before any external collaboration, cloud processing, or publication.

This is a research-use decision based on the competition rules, not legal advice. The rules are controlling. If a planned activity is not clearly permitted, ask Kaggle/H&M for written clarification before proceeding.

## 2. Access decision

**Proposed decision: conditional GO for non-commercial academic research, subject to the user personally accepting the competition rules.**

No dataset was downloaded or accepted on the applicant's behalf. The repository contains only this plan and code that can later read user-provided local files.

Expected local files:
- `articles.csv`
- `customers.csv` (optional; omit from the first experiment)
- `transactions_train.csv`

The images directory is excluded from phase one.

## 3. What the dataset can and cannot support

### It can support
- implicit-feedback recommendation based on historical purchases;
- temporal evaluation of future purchases;
- ranking metrics such as MAP@12, NDCG@K, Recall@K and Precision@K, subject to careful relevance definitions;
- item-attribute-aware recommendation using available article metadata;
- cold-start / low-history slices, if defined before evaluation;
- whether recommendations satisfy user-selected or experimentally defined item constraints.

### It cannot directly establish
- a customer's explicitly stated fashion preferences;
- whether a person likes an item they purchased;
- objective fashion compatibility or universal style rules;
- human-perceived explanation usefulness or trust;
- real-world causal impact on purchases;
- makeup recommendation performance;
- demographic fairness without a separate, justified analysis and ethics review.

Purchases are implicit behavioural observations, not explicit preference statements. Any inferred preference must be labelled as model-inferred, not user-confirmed.

## 4. First-phase attribute mapping

The Kaggle data page describes article metadata. Candidate fields to profile include:

| Source file / field | Candidate OGE-Fashion treatment | Caution |
|---|---|---|
| `articles.csv: article_id` | Stable source identifier for a FashionItem | Keep as a local opaque ID; do not expose user-linked examples |
| `product_type_name` | Candidate item category | Review vocabulary and missingness before mapping |
| `product_group_name` | Broader product category | Do not infer formal taxonomy equivalence |
| `colour_group_name` | Candidate `hasColour` value | Preserve source label; do not infer colour from image |
| `graphical_appearance_name` | Candidate visual-pattern/appearance attribute | Map only after profiling source values |
| `department_name`, `index_name`, `index_group_name`, `section_name`, `garment_group_name` | Candidate classification/context features | Keep separate fields; do not collapse into one ontology class without a reviewed mapping |
| `detail_desc` | Text description evidence | Text-derived attributes require a separate extraction method and validation |
| `transactions_train.csv: customer_id, article_id, t_dat` | Observed purchase interaction / temporal evidence | Not an explicit preference label |
| `price`, `sales_channel_id` | Interaction context | Record currency/scale and meaning from the data documentation before using |
| customer age / postal code | Excluded from initial model | Avoid unnecessary demographic and location processing in phase one |

Before mapping fields into OWL, create a source-to-ontology mapping table with exact values, source provenance, mapping type (exact, broader, narrower, related, unmapped), and reviewer rationale. Do not use `owl:equivalentClass` or `owl:equivalentProperty` based only on label similarity.

## 5. Recommended experiment design

### Research question for this dataset

**Under a fixed temporal evaluation protocol, does adding validated item-attribute and ontology-derived constraint features to an interaction-based fashion recommender improve ranking and constraint satisfaction without unacceptable losses in coverage or diversity?**

This is narrower and more testable than the full research programme. It does not yet test LLM explanation usefulness.

### Data split

- Use the chronological order of transactions.
- Choose train/validation/test cut-offs before tuning; preserve the future test period untouched.
- Prevent future interactions from leaking into user, item, popularity, or feature construction.
- Define how users with no training history and articles first appearing in the test period are handled.
- Use the same eligible customers and candidate set for every model comparison.
- Freeze split logic, filtering, metric definitions and candidate generation before final test evaluation.

The original competition task predicts purchases in a seven-day period immediately after the training data ends and uses MAP@12. This is a useful benchmark reference, but our own train/validation/test design must be documented separately and must not reuse the hidden competition test data.

### Baselines / conditions

1. **Popularity baseline:** globally popular articles computed from training history only.
2. **Collaborative / interaction baseline:** a reproducible implicit-feedback ranker trained only on historical interactions.
3. **Content baseline:** article metadata similarity, with an explicit feature set and a clear cold-start policy.
4. **Ontology-only filter/ranker:** source-mapped item attributes and predeclared constraints, without a learned ranker.
5. **Hybrid:** interaction/content score plus validated ontology-derived features and constraints.

No condition should see future test interactions. Candidate sets, hyperparameter search budgets and evaluation cases should be matched where appropriate.

### Measures

Primary metric candidate: **MAP@12**, because it is the original competition's stated ranking metric. Also report NDCG@12 and Recall@12, plus:
- hard-constraint violation rate;
- catalogue coverage;
- intra-list diversity with a predeclared distance/feature definition;
- performance by interaction-history length;
- runtime and memory under a recorded hardware/software environment.

Report confidence intervals and paired comparisons where appropriate. Do not claim statistical significance unless the statistical test and assumptions are justified.

## 6. Explainability work after the recommender baseline

The real-data phase can support explanations grounded in:
- the exact purchase events available in the user's training history;
- article metadata fields from the catalogue;
- the recommendation model's recorded score components;
- ontology paths derived from the source-to-ontology mapping.

It cannot validate that a customer has an explicit preference unless that preference was supplied or confirmed. Prefer explanation wording such as:

> "Recommended because the item shares the [catalogue attribute] value with items in your recorded purchase history."

Avoid wording such as:

> "You love this style" or "This is your preferred style"

unless the user explicitly stated or confirmed that preference.

The evidence-verifier prototype is currently exact-match and record-ID based. A later version must receive evidence IDs from the actual data pipeline, validate provenance, detect stale/contradictory catalogue data, and test semantic claims. It must not treat model-generated inferences as independent proof.

## 7. Privacy and data handling

- Store raw data outside the Git repository and outside public cloud notebooks.
- Exclude customer age and postal code from phase one.
- Use opaque internal user/item IDs; never publish row-level records or example customer histories.
- Do not attempt re-identification, linkage to external records, or location inference.
- Log aggregate metrics only, with small-group disclosure reviewed before publication.
- Limit access and delete local copies when no longer needed, consistent with applicable rules and institutional policy.
- Obtain institutional guidance on whether ethics review is needed for secondary analysis of the dataset; do not assume public/competition data automatically removes research-ethics obligations.

## 8. Exit gates before results can be reported

1. User has accepted the current Kaggle rules personally.
2. Local data file hashes, file sizes, schema version and access date recorded privately.
3. Data profiling report created without row-level personal data.
4. Missingness, duplicates, item/customer overlap, temporal coverage and long-tail distribution reported.
5. Source field mapping reviewed and versioned.
6. Temporal split and candidate-generation protocol frozen.
7. Baselines run with no test leakage.
8. Results include uncertainty and limitations.
9. Publication/disclosure checked against Kaggle/H&M terms.

Until these gates pass, this plan is a proposed data protocol, not an empirical result.
