# Data Profiling — Initial Makeup Sources
**Version:** 0.1  
**Profile date:** 2026-11-15  
**Status:** Foundation shade source profiled; Open Beauty Facts field coverage pending.

## 1. Purpose
Record reproducible, source-level checks before using candidate makeup datasets. This file contains aggregate profiling results only. It does not contain or redistribute the source CSV, product records, photographs, face images, or participant data.

## 2. The Pudding — makeup-shades

### Source and method
- Source CSV: https://raw.githubusercontent.com/the-pudding/data/master/makeup-shades/shades.csv
- Source README: https://github.com/the-pudding/data/blob/master/makeup-shades/README.md
- Repository licence: https://github.com/the-pudding/data/blob/master/LICENSE
- Access date: 2026-11-15
- Inspection method: read the public CSV from its GitHub source and parse it in memory; no raw CSV was saved to this repository or the user's laptop.
- Source describes 625 foundation swatch records collected from selected brand websites in May 2018. The sample includes selected US, Nigeria, India and Japan product groups.

### Structure and record counts
| Check | Result |
|---|---:|
| Data rows | 625 |
| Columns | 10 |
| Unique brand labels | 36 |
| Unique product labels | 38 |
| Unique brand–product pairs | 39 |
| Unique brand–product–HEX combinations | 621 |
| Blank cells | 0 |
| Invalid six-character HEX values | 0 |
| Repeated brand–product–HEX combinations | 4 repeated records |

Columns present: `brand`, `brand_short`, `product`, `product_short`, `hex`, `H`, `S`, `V`, `L`, `group`.

The repeated combinations identified were:
- Revlon / ColorStay / `d5a187` (source CSV rows 122 and 125).
- Beauty Bakerie / #1 CAKE MIX / `a4683b` (rows 224 and 225).
- Kuddy / Matte Wear / `c78660` (rows 491 and 494).
- Maybelline / Fit Me Matte / `ebba8a` (rows 602 and 611).

These are repeated records in the source. They should be flagged and reviewed before constructing a unique shade catalogue. Do not remove them silently from the preserved source or claim they are accidental without checking source provenance.

### Group distribution
The source README defines the group labels as curated product/brand sampling groups. These are not labels for individual consumers or measured demographic groups.

| Group | Source-defined description | Rows | Share |
|---:|---|---:|---:|
| 0 | Fenty Beauty PRO FILT'R Foundation | 40 | 6.4% |
| 1 | Make Up For Ever Ultra HD Foundation | 40 | 6.4% |
| 2 | US Best Sellers | 167 | 26.7% |
| 3 | BIPOC-recommended brands with BIPOC founders | 85 | 13.6% |
| 4 | BIPOC-recommended brands with white founders | 112 | 17.9% |
| 5 | Nigerian best sellers | 50 | 8.0% |
| 6 | Japanese best sellers | 74 | 11.8% |
| 7 | Indian best sellers | 57 | 9.1% |
| **Total** |  | **625** | **100.0%** |

Do not interpret groups 3 and 4 as user demographic labels. They describe how brands/products were selected for the dataset.

### Numeric and format checks
| Field | Numeric values | Non-numeric/missing values | Observed range |
|---|---:|---:|---:|
| `H` | 613 | 12 values marked `NA` | 4–45 |
| `S` | 613 | 12 values marked `NA` | 0.1–1.0 |
| `V` | 613 | 12 values marked `NA` | 0.2–1.0 |
| `L` | 625 | 0 | 11–95 |

The 12 `NA` values occur in the same 12 records for Covergirl + Olay, product Simply Ageless. The HEX value is present for those records, so colour can still be derived from HEX if the chosen pipeline supports it. Do not impute H/S/V without recording a deterministic derivation method and validation.

### Important source documentation discrepancy
The source README describes `L` as a CIE Lab lightness value represented as a decimal from 0 to 1. The actual CSV values observed in all 625 rows are integers ranging from 11 to 95.

This discrepancy must be resolved before using `L`:
- Do not assume the CSV field has already been normalised to 0–1.
- Do not silently divide values by 100 or otherwise transform them.
- Preserve the original source field and add a separately named derived field only after its scale and transformation are verified.
- Prefer deriving colour coordinates from the source HEX value using a documented and tested colour-conversion implementation, then compare against `L` only after the source field's meaning is clarified.

### Suitability assessment
**Suitable for:**
- A small image-free foundation-shade attribute catalogue.
- Data-cleaning and colour-feature pipeline tests.
- Nearest-colour/shade retrieval baselines using a documented conversion from HEX.
- Catalogue coverage and duplicate-handling experiments.

**Not suitable as standalone ground truth for:**
- Matching a foundation to a person's actual skin colour.
- Ranking preference or satisfaction.
- Consumer preference learning.
- Product efficacy, safety, or ingredient recommendation.
- A modern or comprehensive global foundation catalogue.

The swatches are product-site colour representations from 2018, not instrument-measured skin samples. The dataset has no user ratings, customer interactions, or human preference labels.

## 3. Open Beauty Facts — metadata profiling plan

The official Product Opener documentation states that it powers Open Beauty Facts as a sibling project and that structured API v2 search supports category filters, field selection, and pagination. Search API documentation recommends limiting returned fields and observes a search rate limit. See:
- https://openfoodfacts.github.io/documentation/docs/Product-Opener/v2/search/get-search/
- https://openfoodfacts.github.io/openfoodfacts-server/api/
- https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/tutorial-off-api/

### Status
**No product counts or field-coverage percentages are reported yet.** The live Open Beauty Facts JSON endpoint could not be inspected through the current browser retrieval route. Do not substitute Open Food Facts food-category counts or third-party scraper summaries for actual Open Beauty Facts makeup coverage.

### Planned read-only profile
Use a small, metadata-only query after confirming current Open Beauty Facts endpoint and licence details:
- confirm exact taxonomy slugs for foundation, lipstick, eyeshadow, mascara, blush and other target categories;
- request only fields such as barcode, product name, brands, category tags, ingredients text, allergen tags, countries tags, completeness, and last-modified timestamp;
- avoid image fields and do not download product images;
- record query URL/parameters, date, page/page-size, response counts, and exact product fields returned;
- profile duplicate barcodes, missing values, category coverage, record freshness and ingredient completeness;
- respect official request limits and custom User-Agent requirements;
- preserve ODbL attribution/share-alike obligations where applicable, and separately check rights in product contents and images.

Open Beauty Facts v2 documentation states the endpoint supports `fields`, `page` and `page_size`; the API documentation distinguishes structured category-filter search from full-text search and asks users to limit fields. It also documents read/search rate limits. Confirm the current API deployment and Open Beauty Facts-specific use terms before requests or redistribution.

## 4. Next decision
- Proceed with The Pudding shade data as a small controlled **attribute-retrieval baseline**, after documenting the `L` discrepancy and a duplicate policy.
- Keep Open Beauty Facts at **pending profiling** until the actual makeup-category coverage and required field completeness are measured.
- Do not claim a makeup recommender has been evaluated until real preference/relevance labels and a defensible evaluation protocol exist.
- Keep all source datasets and any future derived data outside this public repository unless their terms explicitly permit distribution.
