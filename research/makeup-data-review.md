# Makeup Data Review
**Review version:** 0.2  
**Review date:** 2026-11-15  
**Status:** Initial source and licence triage; no dataset has been downloaded or approved for model training.

## 1. Decision summary

The first makeup experiments should not depend on face photographs. The most defensible initial combination is:

1. **Foundation shade attributes:** use The Pudding's `makeup-shades/shades.csv` as a small, image-free seed dataset for shade and colour representation. The file contains 625 shade rows, with product/brand identifiers, HEX, HSV, lightness, and a grouping field. The source repository carries an MIT licence. Its README says the source swatch values were collected by visiting selected brand websites in May 2018, covering products selected for the US, Nigeria, India, and Japan. This is a historical sample of product swatches, not a measurement of human skin or a complete makeup recommender. The underlying brand/product identifiers and original source material should still be treated with their own rights and attribution considerations.
2. **Product and ingredient metadata:** assess Open Beauty Facts as a supplementary catalogue source. Its project describes a community-maintained cosmetics database with 100,000+ products from 170 countries, product-label information, ingredients, and allergens. A cloud API profile on 2026-11-15 returned 968 matches for the makeup category tag; the first 100 records had 91% product-name, 95% brand, and 84% ingredient-text coverage, but 0% non-empty allergen tags. The export is listed under ODbL. See data-profiling.md for category and field coverage. Use structured metadata only; do not use product photographs in the first experiment.
3. **Ingredient vocabulary:** consult the European Commission's CosIng database only as a controlled vocabulary/reference for ingredient names and identifiers. CosIng expressly states that it is informational and non-legally binding; an ingredient's presence in the inventory does not mean it is approved for use.

No candidate provides complete, reliable user-preference labels for a makeup recommender. We will need a separately designed preference-evaluation set. Synthetic profiles may test code and ontology rules, but they cannot be presented as evidence of user relevance.

## 2. Candidate assessment

| Candidate | Observed contents | Rights / restrictions found | Fit for OGE-Fashion | Decision |
|---|---|---|---|---|
| **The Pudding — makeup-shades** | 625 foundation shade rows. Fields: `brand`, `brand_short`, `product`, `product_short`, `hex`, `H`, `S`, `V`, `L`, and `group`. One row represents one product shade. | The public repository has a root-level MIT licence; retain the copyright and permission notice when reusing the data. The source README documents swatches collected from selected brand websites in May 2018. Treat brand/product identifiers and upstream source rights separately. | A small image-free shade-attribute seed for colour conversion and diversity baselines. It has no user ratings, measured human skin tones, or preference labels. Its README describes `L` as 0–1, but the CSV values are 11–95; this unresolved source documentation/data discrepancy is documented in [data-profiling.md](data-profiling.md). | **Recommended first seed**, subject to citation and source-rights review. |
| **Open Beauty Facts** | Official project describes 100,000+ cosmetic products from 170 countries, collected by contributors from product labels; ingredients and allergens are among the recorded information. | The Open Beauty Facts export is listed as ODbL on the French open-data portal. ODbL has attribution and share-alike obligations for publicly distributed adapted databases. The Open Food Facts legal guide (same platform/codebase) distinguishes the database licence, individual product contents, and product images; treat the latter separately and confirm the current Open Beauty Facts-specific terms for the records/images actually selected. | Useful for product names, ingredient lists, allergens, and product metadata if the makeup-category fields are sufficiently populated. Community records need completeness and provenance checks. Product-shade values and user preference labels are not guaranteed. | **Recommended supplementary source**, metadata-only at first; record ODbL obligations. |
| **European Commission CosIng** | Official ingredient glossary and information on cosmetic substances/ingredients, including INCI names and identifiers searchable by CAS/ELINCS/EINECS. | Commission page states that the database is informational and has no legal value. Its inventory does not mean an ingredient is approved for use. Check the Commission's reuse notice before redistributing extracted data. | Can help normalize ingredient names and identifiers. It is not a product, shade, or recommendation dataset. | **Reference vocabulary only**, not a recommendation dataset. |
| **BeautyFeeds sample** | Hugging Face sample shows 563 rows and fields including colour, price, category hierarchy, ingredients, product names and image links. | Dataset card declares CC BY-NC 4.0. Retail-source rights and any embedded product-image rights require separate scrutiny. Non-commercial restriction is incompatible with treating it as a cleared commercial catalogue. | Useful for inspecting a possible product schema, but the sample is small and not independent preference ground truth. | **Do not use in deployed product**; optional schema inspection only. |
| **The Beauty API sample** | 1,000-row sample; product details, ingredients, identifiers and product images. Published sample is approximately 131–140 MB depending on the current card revision. | Sample card declares CC BY-NC 4.0. Provider says commercial use requires a separate commercial licence. Full catalogue is a paid/licensed product. | Potential metadata schema reference, but the sample is not a complete independent benchmark and includes a large image payload that is unnecessary for the first experiment. | **Not selected** for initial experiments; revisit only with an appropriate licence. |
| **Innovatiana Cosmetics Retail Dataset (CRD)** | 4,820 annotated in-store cosmetics-retail images and approximately 245,000 CVAT labels. | Provider states research and teaching use only; product images remain property of their respective owners and users must ensure legal conformity. | Intended for retail shelf/product detection, not shade recommendation, makeup look relevance, or user preference modelling. | **Not selected** for the recommender. |
| **BeautyBank / Bare-Makeup Synthesis Dataset (BMS)** | The Hugging Face dataset card lists 319,516 makeup images at 512×512. The WACV 2025 paper describes BMS as 324,000 paired bare/makeup images. These counts describe different artefacts/snapshots and should not be treated as identical. BeautyBank encodes makeup patterns/styles for makeup editing, image encoding, and similarity tasks. | Hugging Face card declares CC BY 4.0 for the distributed BMS files. The bare-face source FFHQ is separately CC BY-NC-SA 4.0 as a dataset, and individual Flickr image licences vary. Do not assume the paired or derivative data is commercially reusable without clarification of the relevant rights. | Useful prior work and possible future visual-style research. It contains face imagery and synthetic makeup transformations, not catalogue product metadata, customer preferences, or product recommendation labels. | **Defer**; not part of the initial recommendation benchmark. |
| **YMU (YouTube Makeup) Dataset** | NIST catalogue describes 151 Caucasian female subjects with before/after makeup images from YouTube tutorials. | The inspected catalogue record does not state a clear reuse licence or access procedure. Original image sources and privacy/consent conditions require clarification. | Face-image dataset with narrow demographic coverage; not product attributes or user-preference labels. | **Exclude from initial work** unless rights, consent, and research necessity are established. |
| **Makeup text dataset (Hugging Face)** | 119 original synthetic examples, augmented to about 1,120 rows; 16 product-type labels. The card says the texts were created as a class exercise and are template/paraphrase based. | Dataset card lists “Carnegie Mellon” as the licence, which is not a clear standard licence identifier. The card itself says it is not representative of real consumer reviews or production recommendation. | Useful only for a small teaching/demo classification exercise; it cannot validate personalisation or recommendation relevance. | **Exclude from evaluation**. |
| **YUVALON makeup_products_1000** | Hugging Face viewer shows 1,000 rows with shade name, category, finish, colour family, undertone, skin-tone-suited labels, rating and HEX fields. | No clear licence or source/provenance statement was found in the dataset listing inspected. | Schema is close to a makeup recommender, but missing rights/provenance make it unsuitable for reuse. The meaning and method behind “skin tones suited” are also not established. | **Do not use** unless the owner supplies licence and provenance evidence. |
| **Mobiusi eyebrow product image dataset** | Hugging Face preview currently exposes only five sample rows, describing eyebrow product type, colour variation and packaging. | CC BY-NC-SA 4.0; the publisher states commercial use requires an additional subscription/authorisation. | Too small and limited to eyebrow products for the intended benchmark. | **Not selected**. |

## 3. Recommended initial data design

### 3.1 Foundation shade seed
See [data-profiling.md](data-profiling.md) for the initial row/field profile, missing-value checks, duplicate combinations, group distribution, and the `L` documentation discrepancy. Use The Pudding shade file to build a small, versioned shade table with:
- source brand and product identifiers;
- source HEX value;
- derived CIE L*a*b* values, with the conversion method and colour-space assumptions recorded;
- source grouping field;
- source date and provenance;
- a missing/uncertain flag for unusable or questionable values.

The CSV contains HEX and HSV/lightness values. The source README describes `L` as a CIE Lab lightness value represented as a decimal from 0 to 1, but the inspected CSV contains integer `L` values from 11 to 95 in all 625 rows. This is a source-documentation/data discrepancy, not a resolved normalization. Do not divide, rescale, or use `L` in experiments until its meaning is clarified. Derive any required colour features from HEX with a separately documented conversion method. Do not relabel any field as a spectrophotometer measurement; these values were extracted from retailer/brand swatches.

CIEDE2000 or another perceptual colour-distance measure may be tested as a nearest-shade baseline after colour conversion is implemented and validated. A colour-distance score is not, by itself, proof that a shade will match a person's skin or be preferred by them.

### 3.2 Product and ingredient metadata
Open Beauty Facts was profiled in a cloud workflow using the documented v2 structured-search endpoint. The general makeup tag returned 968 API matches; the first 100 records had 91% product-name, 95% brand, 100% category-tag, 84% ingredient-text, 0% allergen-tag, 100% country-tag, and 100% last-modified-field coverage. Category-specific counts and coverage are in data-profiling.md. This is first-page sampling, not full-catalogue field coverage. The v2 structured-search API is deprecated, and the v3 documentation currently lists no structured search; do not design a production integration around this endpoint without reassessing API migration.

For the first product-data experiment:
- use text/structured metadata only;
- do not use absence of allergen tags as evidence that a product is allergen-free; initial sample allergen-tag coverage was 0% for the general makeup tag;
- omit product images;
- retain source identifiers and last-modified/provenance data;
- measure missingness and duplicate/variant handling;
- separate observed product-label data from derived classifications;
- do not turn ingredient presence into an unreviewed medical or safety recommendation.

ODbL implications must be documented before publishing a derived product database. If a public derivative database is distributed, preserve required attribution, share-alike, and keep-open obligations. Get a proper licence review before deciding how catalogue data will be packaged in a commercial product.

### 3.3 Ingredient terminology
CosIng can be considered for controlled ingredient labels and identifiers. It must not be used as a binary “safe/approved” signal. The European Commission expressly warns that an INCI name appearing in the inventory does not itself mean the ingredient is approved for cosmetic use.

### 3.4 User preference and evaluation data
None of the sources above supplies a complete, reliable set of individual user preferences for fashion/makeup recommendation.

Plan a separate evaluation dataset:
- begin with synthetic profiles to test application logic, filters and ontology queries only;
- define explicit preference fields (product category, colour family, finish, coverage, price range, excluded ingredients where appropriately justified, and occasion);
- design a consent-based preference and pairwise-choice protocol for adult participants;
- obtain required institutional ethics review/approval before recruitment;
- avoid collecting face images or inferring sensitive attributes;
- record participant consent, withdrawal and deletion procedures;
- report the sample composition and limitations.

Human preferences must not be invented or generated by treating product metadata as user feedback.

## 4. Recommended scope for the first makeup experiment

**Experiment M1 — Foundation shade attribute matching**
- Input: a user-selected or manually supplied target colour preference.
- Catalogue: the 625-row The Pudding shade seed.
- Candidate baseline: nearest-neighbour colour distance in a documented colour space.
- Output: ranked product shades with source attributes and distance-based explanation.
- Evaluation: first validate colour conversion and data quality; then compare ranked alternatives against human preference judgements only after a suitable participant protocol is approved.

**Experiment M2 — Makeup product metadata retrieval**
- Input: explicit category and user-selected filters.
- Catalogue: an approved Open Beauty Facts metadata subset, if makeup categories and required product fields pass profiling.
- Method: ontology-aware filtering and structured attribute matching before considering learned ranking.
- Evaluation: query coverage, constraint violations, field completeness, and later user relevance.

**Cross-domain fashion-plus-makeup matching is deferred** until the fashion and makeup domains each have a defensible attribute representation and evaluation labels. Do not create synthetic pairings and then report them as real-world compatibility evidence.

## 5. Data storage and cloud handling

- Keep raw or restricted datasets outside this public repository.
- Do not commit dataset CSV exports, images, product photos, model checkpoints, participant data, or credentials.
- Store source URLs, licence decisions, data dictionaries and permitted checksums in Git.
- Use a cloud notebook or Codespace for inspection and processing; do not download datasets onto the laptop.
- Use a small synthetic fixture for automated tests.
- Do not place API credentials in notebooks or repository files. Use environment-level secrets only when a real API integration is required.

## 6. Source register and access links

### Recommended initial sources
- The Pudding dataset directory: https://github.com/the-pudding/data/tree/master/makeup-shades
- The Pudding shade CSV: https://github.com/the-pudding/data/blob/master/makeup-shades/shades.csv
- The Pudding source README and collection method: https://github.com/the-pudding/data/blob/master/makeup-shades/README.md
- The Pudding repository MIT licence: https://github.com/the-pudding/data/blob/master/LICENSE
- Open Beauty Facts official project and source repository: https://github.com/openfoodfacts/openbeautyfacts
- Open Beauty Facts data portal: https://world.openbeautyfacts.org/data
- Open Beauty Facts export listing and licence: https://www.data.gouv.fr/datasets/open-beauty-facts
- Official ODbL 1.0 text: https://opendatacommons.org/licenses/odbl/1-0/
- Open Food Facts legal guide distinguishing database, individual contents, and images: https://openfoodfacts.github.io/openfoodfacts-server/api/tutorials/license-be-on-the-legal-side/
- European Commission CosIng: https://single-market-economy.ec.europa.eu/sectors/cosmetics/cosmetic-ingredient-database_en
- European Commission data reuse notice: https://data.europa.eu/en/legal-notice

### Other candidates reviewed
- BeautyFeeds sample: https://huggingface.co/datasets/beautyfeeds/beautyfeeds_sample_data
- The Beauty API sample: https://huggingface.co/datasets/thebeautyapi/beautyproducts
- Innovatiana Cosmetics Retail Dataset: https://www.innovatiana.com/en/datasets/innovatianas-cosmetics-retail-dataset-crd
- BeautyBank paper: https://openaccess.thecvf.com/content/WACV2025/html/Lu_BeautyBank_Encoding_Facial_Makeup_in_Latent_Space_WACV_2025_paper.html
- Bare-Makeup Synthesis Dataset card: https://huggingface.co/datasets/lulululululululululu/Bare-Makeup-Synthesis-Dataset
- FFHQ project and dataset terms: https://github.com/NVlabs/ffhq-dataset
- YMU NIST catalogue record: https://tsapps.nist.gov/BDbC/Search/Details/343
- Makeup text dataset: https://huggingface.co/datasets/keerthikoganti/makeup-text-dataset
- YUVALON makeup products sample: https://huggingface.co/datasets/YUVALON/makeup_products_1000.csv
- Mobiusi eyebrow product image dataset: https://huggingface.co/datasets/Mobiusi/Eyebrow-Makeup-Product-Image-Classification-Dataset

## 7. Decision log

See [data-profiling.md](data-profiling.md) for the observed profile of The Pudding CSV. The Open Beauty Facts profile remains pending; no category counts or field completeness figures are claimed.

| Decision | Status | Rationale |
|---|---|---|
| Start without face images | Decided | Product metadata and shade swatches are sufficient for the first experiments; reduces privacy and licensing risk. |
| Use The Pudding shade data as initial seed | Recommended | Clear repository MIT licence, 625 structured shade records, no face images. |
| Assess Open Beauty Facts metadata as product catalogue source | Conditional GO for metadata-only prototype | 968 API matches for makeup tag; first 100 had 84% ingredient-text coverage but 0% allergen-tag coverage. ODbL obligations and deprecated v2 search endpoint require caution. |
| Use product images in the first experiment | Excluded | Not necessary for shade/ingredient metadata and each image has separate rights. |
| Use BeautyBank/YMU face images in the initial model | Excluded | Not needed for the initial research questions; distinct licence, consent, and representation risks. |
| Treat synthetic profiles as user-study evidence | Excluded | Synthetic profiles test software only, not real user relevance. |
| Build linked fashion–makeup recommendations immediately | Deferred | Need defensible domain-specific labels and evaluation in each domain first. |

## 8. Review limitations
This is a first-pass dataset triage, not legal advice or a complete catalogue of available datasets. Listings, licences and provider terms can change. The Pudding seed is old and narrow. Open Beauty Facts is community-contributed and requires a data-quality audit. The cloud profile queried metadata in memory and retained aggregate statistics only; no raw export, product records, barcode list, images, or product photos were committed. No recommendation model has been trained on these records.
