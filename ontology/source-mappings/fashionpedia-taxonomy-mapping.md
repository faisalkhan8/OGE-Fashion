# Fashionpedia taxonomy extraction and OGE-Fashion mapping

**Status:** Initial source-aligned mapping draft, 2026-11-15  
**Source taxonomy manifest:** [category_attributes_descriptions.json](https://github.com/KMnP/fashionpedia-api/blob/master/data/demo/category_attributes_descriptions.json)  
**Primary project:** https://fashionpedia.github.io/home/index.html  
**Official terms:** https://fashionpedia.github.io/home/data_license.html  
**Paper:** Jia et al. (2020), *Fashionpedia: Ontology, Segmentation, and an Attribute Localization Dataset*, ECCV 2020.

## Extracted structure

The source manifest contains **46 category records** and **294 attribute records**. The official project describes these as 27 main apparel categories, 19 apparel parts, and 294 fine-grained attributes.

The 46 category records are represented with three source-supercategory groups for the 19 part-related entries:

| Source supercategory | Records |
|---|---:|
| upperbody | 6 |
| lowerbody | 3 |
| wholebody | 4 |
| head | 3 |
| neck | 1 |
| arms and hands | 2 |
| waist | 1 |
| legs and feet | 4 |
| others | 3 |
| garment parts | 7 |
| closures | 2 |
| decorations | 10 |

The attribute records are grouped into 11 source-defined supercategories:

| Source supercategory | Records | OGE-Fashion target class |
|---|---:|---|
| animal | 6 | `oge:AnimalPatternAttribute` |
| leather | 4 | `oge:LeatherAttribute` |
| length | 15 | `oge:GarmentLengthAttribute` |
| neckline type | 25 | `oge:NecklineTypeAttribute` |
| nickname | 153 | `oge:GarmentNicknameAttribute` |
| non-textile material type | 10 | `oge:NonTextileMaterialTypeAttribute` |
| opening type | 10 | `oge:OpeningTypeAttribute` |
| silhouette | 25 | `oge:GarmentSilhouetteAttribute` |
| textile finishing, manufacturing techniques | 21 | `oge:TextileFinishingTechniqueAttribute` |
| textile pattern | 18 | `oge:TextilePatternAttribute` |
| waistline | 7 | `oge:WaistlineAttribute` |

## Modelling decision

The source separation between categories and attributes is preserved. The 27 main apparel entries become individuals typed as `MainApparelCategory`; the 19 part-related entries become individuals typed as `GarmentPartCategory`, `ClosureCategory`, or `DecorationCategory` according to their source supercategory. Each of the 294 source attribute entries becomes a named individual typed by an OGE-Fashion class mapped from its source attribute supercategory.

Every individual preserves:
- source-local ID;
- source taxonomy ID;
- exact source label;
- source supercategory;
- source taxonomy level;
- source manifest URL.

The 340 labels are therefore represented as controlled individuals rather than 340 new OWL classes. The source supercategory strings are retained as provenance metadata; they are not automatically converted into OWL subclass axioms.

## Attribute group mapping

| Fashionpedia supercategory | OGE-Fashion class | Interpretation |
|---|---|---|
| nickname | `GarmentNicknameAttribute` | Preserve source-defined garment nickname/type descriptors without reinterpreting each term |
| silhouette | `GarmentSilhouetteAttribute` | Silhouette descriptors |
| waistline | `WaistlineAttribute` | Waistline descriptors |
| length | `GarmentLengthAttribute` | Garment length descriptors |
| neckline type | `NecklineTypeAttribute` | Neckline descriptors |
| opening type | `OpeningTypeAttribute` | Garment opening descriptors |
| non-textile material type | `NonTextileMaterialTypeAttribute` | Source-defined non-textile material descriptors |
| leather | `LeatherAttribute` | Source-defined leather-related descriptors |
| textile finishing, manufacturing techniques | `TextileFinishingTechniqueAttribute` | Textile finishing/manufacturing descriptors |
| textile pattern | `TextilePatternAttribute` | Textile pattern descriptors |
| animal | `AnimalPatternAttribute` | Animal-pattern descriptors as shown by source labels |

These OGE-Fashion classes are project modelling choices, not claims of exact equivalence to Fashionpedia OWL classes. No `owl:sameAs`, `owl:equivalentClass`, or `owl:equivalentProperty` assertions are introduced.

## Provenance and licensing

The source extraction copied taxonomy metadata only. No Fashionpedia images, masks, face images, or participant data were copied.

The Fashionpedia project's official Terms of Use state that its ontology and annotations are licensed under Creative Commons Attribution 4.0. The API repository's BSD-style `license.txt` applies to API software and is not treated as the data licence. Images are excluded: Fashionpedia says it does not own image copyright and use of images must follow the original image-provider terms.

Attribution: Jia, M., Shi, M., Sirotenko, M., Cui, Y., Cardie, C., Hariharan, B., Adam, H., and Belongie, S. (2020). *Fashionpedia: Ontology, Segmentation, and an Attribute Localization Dataset*. ECCV 2020. https://fashionpedia.github.io/home/index.html. Licensed under CC BY 4.0 for the ontology and annotations: https://creativecommons.org/licenses/by/4.0/.

## Limits

1. This is source-term preservation and structural alignment, not a claim that OGE-Fashion and Fashionpedia are semantically identical.
2. No hierarchy beyond the source group data is inferred.
3. This mapping does not provide makeup terms, user preferences, compatibility rules, or recommendation labels.
4. The taxonomy manifest is not an interaction dataset and does not validate recommendation relevance.
5. Detailed exact/broader/narrower relation testing against every source OWL concept remains a subsequent alignment task.

## Files

- `fashionpedia-categories.csv`: all 46 source categories and their OGE target classes.
- `fashionpedia-attributes.csv`: all 294 source attributes and their OGE target classes.
- `../oge-fashion-v0.1.ttl`: OWL/Turtle ontology with the source-aligned individuals.
