# Dataset and Data-Source Register
**Version:** 0.4 — first-pass source and licence review, not legal advice or final clearance.

## Acceptance checklist
A source may be used only after its identity, access conditions, licence, permitted purposes, redistribution limits, attribution, provenance, and suitability for the planned research are recorded. Public download availability does not imply commercial reuse rights. The licence for annotations/metadata may differ from the licence for underlying images.

## Candidate register

| Source | Potential role | Primary-source finding | Research-use position | Public/commercial product position | Status |
|---|---|---|---|---|---|
| Fashionpedia annotations and ontology | Clothing categories, parts, fine-grained visual attributes, ontology design | Official project page states annotations and ontology are CC BY 4.0. It says the project does not own image copyrights; images originate from third-party platforms and remain subject to their terms. | Annotations/ontology may be reusable with CC BY 4.0 attribution. Images need separate source-by-source review. | Do not assume all images may be republished or commercially deployed. | **Conditional** — annotation/ontology rights clearer; image rights unresolved per image. |
| Fashionpedia software | Data/API tooling | Official page supplies a separate source/binary redistribution notice. | Review the exact notice before reusing code. | Do not conflate software terms with image or ontology rights. | **Conditional** — verify notice before copying code. |
| DeepFashion | Clothing attributes, retrieval, landmarks and related tasks | Official dataset page states non-commercial research only. Release agreement restricts commercial exploitation and redistribution of data/derived portions. | Potential research use only after access approval and signed agreement; restrictions on derivative outputs need clarification. | **Do not use for public/commercial product without separate written permission.** | **Restricted / pending access**. |
| The Pudding — makeup-shades | Foundation shade and colour attributes | The public CSV has 625 rows, with brand/product, HEX, HSV, lightness and group fields. Its README says source swatches were collected from selected brand sites in May 2018 across the US, Nigeria, India and Japan. The root repository includes an MIT licence. | Suitable as a small, image-free shade-attribute seed with source attribution. It does not provide user ratings, measured skin tones, or preference labels. The `L` field is source-defined as a 0–1 CIE Lab lightness value; do not assume it is untransformed CIE L*. | Retain the repository MIT notice; treat brand/product references and upstream swatch source rights separately before commercial deployment. | **Recommended initial seed**. |
| Open Beauty Facts | Makeup/cosmetics product metadata, ingredients, allergens, product labels | Official project describes 100,000+ products from 170 countries, contributed from product labels. Its export is listed as ODbL on data.gouv.fr. The shared Open Food Facts legal guide distinguishes database rights, individual contents, and product-image rights; verify current OBF-specific terms for selected records/images. | Useful supplementary metadata if makeup category coverage and fields pass profiling. Preserve ODbL attribution/share-alike obligations for any publicly distributed adapted database. | Do not assume the database, each product record, and each photo share identical terms. Confirm OBF-specific rights and image/third-party content before product deployment. | **Recommended metadata source; pending profiling**. |
| European Commission CosIng | Ingredient names and identifiers | Official database lists common cosmetic ingredient names and related information. The Commission states it is informative and has no legal value; an INCI entry does not itself mean an ingredient is approved for use. Commission reuse policy generally permits EU-owned editorial content under CC BY 4.0 unless otherwise noted, but third-party rights may require separate permission. | Can support ingredient-name normalization after checking the rights attached to the specific data/reuse route. | Never present an inventory entry as a safety approval or compliance result. | **Reference vocabulary only**. |
| BeautyFeeds sample | Product names, categories, colours, ingredients, listings | Hugging Face dataset card shows 563 rows and fields including colour/category/ingredients; card states CC BY-NC 4.0. | Schema inspection or non-commercial research only, subject to verifying upstream retailer content rights. | Not cleared for commercial product use. | **Not selected**. |
| The Beauty API sample | Product metadata, ingredient data, images | 1,000-row sample; card states CC BY-NC 4.0. Provider states a separate commercial licence is required for commercial access/use. | Could be inspected for schema in non-commercial research if needed. | Do not use in deployed product without a separate commercial licence. | **Not selected**. |
| Innovatiana Cosmetics Retail Dataset | In-store shelf/object detection | 4,820 annotated images and approx. 245,000 labels; provider says research/teaching only and that images remain owned by their respective owners. | Research/teaching use subject to terms. | No product deployment without image-owner rights. | **Not suitable for recommendation task**. |
| BeautyBank / BMS | Makeup-style image encoding and synthesis | BMS card lists 319,516 makeup images and CC BY 4.0. BeautyBank paper describes paired bare/makeup synthesis and 1,412 encoded makeup styles. Bare-face images link to FFHQ; FFHQ has CC BY-NC-SA 4.0 dataset terms and per-image licences vary. | Possible future visual-style research after rights review. Not a product catalogue or user preference dataset. | Do not assume commercial reuse of paired/derivative face data. | **Deferred**. |
| YMU (YouTube Makeup) | Before/after makeup face images | NIST record describes 151 Caucasian female subjects from YouTube makeup tutorials. The inspected record does not state a clear reuse licence or access process. | Do not use until owner/source rights and consent/access terms are confirmed. | Not cleared. | **Excluded from initial work**. |
| Makeup text dataset | Text classification by makeup product type | Dataset card states 119 original synthetic examples, augmented to approx. 1,120 rows, and 16 labels; its own card warns it is not representative of real consumer data. | Small teaching/demo use only; licence string is not a clear standard licence. | Not suitable for production or recommendation evaluation. | **Excluded**. |
| YUVALON makeup_products_1000 | Product shade/finish/skin-tone metadata | Viewer shows 1,000 rows with shade, colour, undertone, finish, ratings and skin-tone fields; no clear licence/provenance was found in the listing. | Do not use without explicit licence and source evidence. | Not cleared. | **Excluded pending rights evidence**. |
| Mobiusi eyebrow product images | Eyebrow product image classification | Viewer currently exposes five sample rows; card states CC BY-NC-SA 4.0 and commercial use requires further authorisation. | Too small for a representative evaluation. | Not cleared for commercial use. | **Not selected**. |

## Fashionpedia — detailed review
Primary source: https://fashionpedia.github.io/home/data_license.html

The official page distinguishes:
1. **Annotations and ontology:** CC BY 4.0.
2. **Software:** separate source/binary redistribution conditions.
3. **Images:** the project says it does not own image copyright. Use is subject to the terms of the original sources.

### Decision
- Fashionpedia's ontology and annotation layer is a strong candidate for fashion vocabulary alignment, subject to attribution.
- Do not mirror images into this public repository.
- Before training or deployment, review rights for the exact image subset and sources.
- Preserve source attribution and licence information.

## DeepFashion — detailed review
Primary sources:
- Dataset page: https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html
- Release agreement: https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion/DeepFashionAgreement.pdf

The official page states non-commercial research only. The release agreement restricts commercial exploitation and further distribution of portions and derived data. Access instructions require a completed agreement.

### Decision
- Treat as research-only and restricted.
- Do not include assets in GitHub or a deployed product.
- Do not publish derived data until the agreement's implications are clarified.
- No access request or download has been made.

## Makeup data — detailed review
See [Makeup Data Review](makeup-data-review.md) for the candidate-by-candidate assessment, source rights, and initial experiment design.

### Current recommendation
- Use The Pudding's MIT-licensed foundation-shade table as the initial, image-free shade seed.
- Assess Open Beauty Facts for supplementary product and ingredient metadata, preserving ODbL requirements and avoiding product photos in the first experiment.
- Use CosIng only as an ingredient vocabulary/reference, not as a regulatory approval signal.
- Collect no user/face images for the first makeup experiments.
- Treat preference labels as a separate research requirement; do not infer them from product catalogue data.

## Required record per source
For each source, retain official URL, owner/publisher, version/access date, citation, full licence/terms, permitted research/commercial/modification/redistribution uses, attribution, personal-data/consent concerns, fields/label definitions, known bias, intended role, and final decision. For Open Beauty Facts, separate the ODbL database, individual database contents, and photographs/third-party artwork; the linked general legal guide is for the shared platform, so verify OBF-specific terms for actual records before deployment.

## Data segregation
- Keep raw/restricted data outside the public Git repository.
- Commit schemas, data dictionaries, source manifests, synthetic examples, and permitted metadata only.
- Do not publish user/face images, scraped personal data, or dataset assets without explicit rights.
- Keep research-only data separate from material intended for public/commercial deployment.

## Remaining actions
1. Profile The Pudding foundation-shade CSV in a cloud workspace; do not commit the raw data file.
2. Sample Open Beauty Facts records and measure makeup-category coverage, field completeness, duplicate variants, and provenance.
3. Confirm exact OBF terms for the current export and product-image/individual-content rights before any deployment.
4. Map selected shade/product fields to the ontology, preserving source and licence provenance.
5. Define a separate, ethics-reviewed user-preference evaluation protocol.
