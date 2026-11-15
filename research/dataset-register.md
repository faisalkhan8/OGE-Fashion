# Dataset and Data-Source Register
**Version:** 0.2 — first-pass primary-source review, not legal advice or final clearance.

## Acceptance checklist
A source may be used only after its identity, access conditions, licence, permitted purposes, redistribution limits, attribution, provenance, and suitability for the planned research are recorded. Public download availability does not imply commercial reuse rights. The licence for annotations/metadata may differ from the licence for underlying images.

## Candidate register

| Source | Potential role | Primary-source finding | Research-use position | Public/commercial product position | Status |
|---|---|---|---|---|---|
| Fashionpedia annotations and ontology | Clothing categories, parts, fine-grained visual attributes, ontology design | The official licence page says annotations and ontology are CC BY 4.0. It reports that the project does not own image copyrights; images originate from Flickr, Unsplash, Burst by Shopify, Freestocks, Kaboompics and Pexels and must follow those providers' terms. The project places responsibility for image use on dataset users. | The annotations/ontology appear reusable under CC BY 4.0 with attribution and licence obligations. Image use requires a separate source-by-source review and adherence to each provider's terms. | Do not assume all images may be republished or commercially deployed. Evaluate each image/source and the applicable terms; exclude assets without clear rights. | **Conditional** — annotation/ontology rights clearer; image rights unresolved per image. |
| Fashionpedia software | Data/API tooling | The official page supplies a separate source/binary redistribution notice with two conditions and disclaimer. | Review the exact notice and retain required copyright/license text if software is reused. | Same source/binary notice conditions apply; do not conflate software terms with image rights. | **Conditional** — verify exact notice before copying code. |
| DeepFashion | Clothing categories, 1,000 descriptive attributes, bounding boxes, landmarks, retrieval/attribute prediction research | Official dataset page states non-commercial research only. Release agreement prohibits commercial exploitation of images and portions of derived data, and further copying, publishing, or distributing any portion of the dataset. Images were obtained from the Internet and are not owned by MMLAB. Access instructions require completing/signing the release agreement and emailing it to the dataset contacts; page specifies institutional email. | Potentially available for non-commercial research after access approval and agreement. Do not redistribute images. Assess whether any derived outputs can be shared before publication. | **Do not use for a public/commercial product absent separate written permission.** The agreement's derived-data and redistribution restrictions need careful interpretation for any planned publication artefact. | **Restricted / pending access** — signed agreement and intended-use clarification required. |
| Polyvore outfit compatibility data | Outfit compatibility and composition | No current owner-approved access route or licence has been verified in this review. | Not approved until a reliable source and licence are found. | Not approved. | **Unverified candidate**. |
| Makeup datasets | Makeup categories/styles/attributes | No specific dataset has yet passed source and licence review. | No approved dataset yet. | No approved dataset yet. | **Open task**. |
| Curated catalogue metadata | Ontology prototype and controlled recommendation evaluation | Could be built from sources with explicit reuse permission or original annotations, but would require provenance and annotation rules. | Viable fallback for synthetic/prototype work; real research labels need a documented protocol and adequate evaluation design. | Only use metadata/images with explicit rights for product use. | **Possible fallback; not yet created**. |

## Fashionpedia — detailed review
Primary source: https://fashionpedia.github.io/home/data_license.html

The official page distinguishes:
1. **Annotations and ontology:** CC BY 4.0. Attribution and compliance with the licence are required.
2. **Software:** separate source/binary redistribution conditions and disclaimer. Read the exact notice before reusing code.
3. **Images:** the project says it does not own image copyright. It directs users to the terms of the original image sources: Flickr, Unsplash, Burst by Shopify, Freestocks, Kaboompics, and Pexels. It states that users accept responsibility for image use, including copies of copyrighted images.

### Decision
- Fashionpedia's ontology and annotation layer is the best-supported first data resource for the **fashion attribute vocabulary** and may be used subject to CC BY 4.0 obligations.
- Do not mirror its images into this public repository.
- Before training, cloud storage, demo, or commercial deployment, make an image-level/source-level rights decision for the exact subset used. Dataset-level aggregation does not automatically grant one uniform image licence.
- Keep the annotation/ontology attribution and licence notice with any permitted derived distribution.

## DeepFashion — detailed review
Primary sources:
- Dataset page: https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html
- Release agreement: https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion/DeepFashionAgreement.pdf

The official page states that the dataset is available for non-commercial research only. Its release agreement prohibits commercial exploitation of any portion of the images or derived data, and prohibits further copying, publishing, or distributing any portion of the dataset. It also says the images were obtained from the Internet and are not owned by MMLAB. The access instructions ask applicants to complete and sign the agreement and email it to the listed contacts using an institutional email address.

### Decision
- Treat as research-only and restricted.
- Do not include images or dataset portions in GitHub, public demos, or deployed product.
- Do not publish a derived-data artefact until the exact agreement implications are clarified.
- Before pursuing access, clarify whether an independent researcher/industry-affiliated researcher without an institutional email is eligible, and whether the proposed publication outputs are permitted.
- No agreement has been signed and no dataset access has been requested as part of this review.

## Required record per source
Record dataset name, official URL, owner/publisher, version/access date, citation, full licence and terms, allowed research/commercial/modification/redistribution uses, attribution, personal-data/consent issues, fields/label definitions, known bias, intended role, and final decision (approved, restricted, rejected, or pending).

## Data segregation
- Keep raw/restricted data outside the public Git repository.
- Commit schemas, data dictionaries, source manifests, synthetic examples, and permitted metadata only.
- Do not publish user/face images, scraped personal data, or dataset assets without explicit rights.
- Keep research-only data separate from material intended for public/commercial deployment.

## Remaining actions
1. Complete Fashionpedia image-source rights review for any intended subset.
2. Confirm exact attribution and compliance steps for any reuse of Fashionpedia annotations/ontology.
3. Decide whether to request DeepFashion access; seek written clarification of research status and permissible outputs first.
4. Identify and assess makeup dataset candidates.
5. Do not begin training against unverified dataset access.
