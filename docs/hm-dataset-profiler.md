# H&M dataset aggregate profiler

This script profiles only the two CSV files needed for the first fashion-domain recommender experiment:

- `articles.csv`
- `transactions_train.csv`

It does not read `customers.csv` or the image archive. It streams transaction rows, validates required columns, counts missing/invalid fields, checks whether each transaction's article ID appears in the article catalogue, records transaction-date bounds, and calculates file hashes.

## Access and data terms

The dataset is not included in this repository. Before downloading or analysing it, personally register at Kaggle and accept the current H&M competition rules. The rules permit non-commercial academic research but prohibit sharing or redistributing the competition data with people who have not accepted the rules.

Keep both CSVs and any generated local profile under an ignored local path such as `data/raw/hm/`. Do not commit raw data, row-level samples, customer IDs, article IDs, product descriptions, or private profile reports.

Official data description: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data  
Official rules: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/rules

## Usage

After downloading the permitted CSV files to a local directory:

```bash
python scripts/profile_hm_dataset.py --data-dir data/raw/hm
```

To save the aggregate report locally:

```bash
python scripts/profile_hm_dataset.py \
  --data-dir data/raw/hm \
  --output data/raw/hm/hm-profile.local.json
```

The report contains aggregate counts, date bounds, file sizes, hashes and missingness counts. Hashes are useful for tracking the exact local input version; do not publish a report unless the data terms and disclosure implications have been reviewed.

## Scope limitations

- The profiler does not train a recommender or produce research results.
- Purchase events are implicit behavioural observations, not explicit user preferences.
- It omits customer age, postal code and the optional images from the first phase.
- It does not determine whether a catalogue attribute is semantically correct; source-to-ontology mappings still require review.
- A successful profile does not imply that the dataset is suitable for every research question or publication use.
