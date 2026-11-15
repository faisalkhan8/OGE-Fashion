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

## 3. Open Beauty Facts — live metadata profile

**Profile workflow:** https://github.com/faisalkhan8/OGE-Fashion/actions/runs/43722932460  
**Profile timestamp:** 2026-11-15 14:07:16 UTC  
**API:** `https://world.openbeautyfacts.org/api/v2/search`  
**Method:** nine structured category-tag queries; page 1; page size 100; metadata-only fields; six-second delay between category requests; descriptive User-Agent. No image fields were requested.

### Category counts returned by the API

| English category tag | API matching count | Records sampled on page 1 |
|---|---:|---:|
| makeup | 968 | 100 |
| cosmetics | 137 | 100 |
| face-makeup | 250 | 100 |
| lip-makeup | 115 | 100 |
| mascara | 88 | 88 |
| foundation | 66 | 66 |
| lipstick | 60 | 60 |
| eyeshadow | 26 | 26 |
| make-up | 3 | 3 |

All nine category queries succeeded. These values are counts returned for each category filter at the profile timestamp. They **must not be summed**: category tags are hierarchical/overlapping, so a product can be counted in more than one query. The counts are not a count of unique products across all categories.

### Field coverage in the first-page samples

Percentages below are calculated within the records returned for each category (maximum 100). They describe presence of non-empty fields, not correctness or completeness of the underlying product description.

| Category tag | Sample n | Product name | Brand | Category tags | Ingredients text | Allergen tags | Country tags | Last modified |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| makeup | 100 | 91.0% | 95.0% | 100% | 84.0% | 0% | 100% | 100% |
| cosmetics | 100 | 89.0% | 81.0% | 100% | 22.0% | 1.0% | 100% | 100% |
| face-makeup | 100 | 95.0% | 98.0% | 100% | 79.0% | 0% | 100% | 100% |
| lip-makeup | 100 | 90.0% | 89.0% | 100% | 71.0% | 8.0% | 100% | 100% |
| mascara | 88 | 97.7% | 93.2% | 100% | 48.9% | 2.3% | 98.9% | 100% |
| foundation | 66 | 100% | 100% | 100% | 90.9% | 4.5% | 100% | 100% |
| lipstick | 60 | 91.7% | 86.7% | 100% | 68.3% | 18.3% | 100% | 100% |
| eyeshadow | 26 | 96.2% | 92.3% | 100% | 69.2% | 0% | 100% | 100% |
| make-up | 3 | 66.7% | 33.3% | 100% | 33.3% | 0% | 100% | 100% |

### Barcode checks

- No returned record in any of the nine first-page samples was missing a barcode.
- No repeated barcode rows were observed within any individual category sample.
- This is a first-page sample check only; it does not establish catalogue-wide uniqueness.
- Samples from different category queries can overlap. No unique cross-category union count was calculated.

### Query fields and data handling

Requested fields were: `code`, `product_name`, `brands`, `categories_tags`, `ingredients_text`, `allergens_tags`, `countries_tags`, and `last_modified_t`.

No images or image URLs were requested. The profiler processes the returned product metadata in memory and emits only aggregate counts and field coverage. It does not write API product records, barcodes, names, or photographs to the repository.

### API lifecycle limitation

The official Product Opener documentation currently labels API v2 deprecated. It also states that structured category-filter search is available through `/api/v2/search`, while structured search is not available in the current v3 API documentation. This profile therefore uses the documented v2 structured-search route as a research snapshot, not as a long-term production integration. Recheck the API migration path before building a deployed catalogue importer.

Official API references:
- https://openfoodfacts.github.io/documentation/docs/Product-Opener/v2/search/get-search/
- https://openfoodfacts.github.io/openfoodfacts-server/api/

### Go / no-go decision

**Conditional GO for a metadata-only catalogue prototype.** The general `makeup` tag returned 968 matching products, with the first 100 records showing 91% product-name coverage, 95% brand coverage, and 84% ingredient-text coverage. This is sufficient to justify a small metadata retrieval and ontology-mapping experiment, subject to ODbL and source-content rights review.

**NO-GO for allergy or safety decisions.** The `makeup` sample had 0% non-empty `allergens_tags`, and allergen-tag coverage stayed low across all queried categories (0–18.3%). Ingredient text is also incomplete and unverified. Do not use absence of an allergen tag as evidence that a product is allergen-free, and do not generate medical/safety claims from these records.

The profile is not a recommendation evaluation. It contains no user ratings, preference feedback, or human relevance judgements. Category counts and first-page field coverage cannot be treated as evidence of consumer preference or product quality.

## 4. Next decision
- Proceed with The Pudding shade data as a small controlled **attribute-retrieval baseline**, after documenting the `L` discrepancy and a duplicate policy.
- Use Open Beauty Facts conditionally for metadata-only prototyping: the `makeup` tag returned 968 matches and the first 100 records had 84% ingredient-text coverage. Do not use it for allergen/safety decisions because allergen-tag coverage is very low, and do not treat its metadata as user preference labels.
- Do not claim a makeup recommender has been evaluated until real preference/relevance labels and a defensible evaluation protocol exist.
- Keep all source datasets and any future derived data outside this public repository unless their terms explicitly permit distribution.

## 5. Foundation shade baseline — GitHub Actions smoke run

**Workflow run:** https://github.com/faisalkhan8/OGE-Fashion/actions/runs/43723048053  
**Commit tested:** `638205d9f7459c77b2a714ba7bab930eccf218bd`  
**Runtime:** GitHub-hosted Ubuntu runner, Python 3.12.16  
**Result:** successful.

### Test results
- 15 unit tests passed, including an aggregate-profile test for Open Beauty Facts field coverage and duplicate-barcode diagnostics.
- Eight published CIEDE2000 reference pairs passed within 0.0001 of their rounded expected values.
- sRGB-to-CIELAB tests for black, white, and red passed.
- Parser tests for duplicate handling, missing H/S/V, disputed L-column exclusion, and invalid source fields passed.
- Sample ranking completed after fetching the pinned CSV from upstream at runtime.

### Example ranking
Reference swatch: `F3CFB3`  
Metric: CIEDE2000 (lower means closer displayed swatch colour).

| Rank | Brand / product | Source HEX | Delta E00 |
|---:|---|---|---:|
| 1 | Maybelline / Fit Me | F3CFB3 | 0.0000 |
| 2 | Fenty / PRO FILT'R | FAD5B8 | 1.4504 |
| 3 | Kate / Secret Skin Maker Zero | F7D5BB | 1.5172 |
| 4 | Make Up For Ever / Ultra HD | EBCAB0 | 1.5905 |
| 5 | Maybelline / Fit Me Matte | F9D0B0 | 1.6160 |

The first result is an exact swatch already present in the source catalogue, so the zero distance is expected. This run validates fetching, parsing, duplicate handling, colour conversion, distance calculation, deterministic ranking, and command-line execution. It does **not** validate recommendation relevance, foundation suitability, real-world skin matching, or consumer preference.

The workflow uses the Python standard library; it does not store the source CSV, product images, model files, or participant information in the repository.
