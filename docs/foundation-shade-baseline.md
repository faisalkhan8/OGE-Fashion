# Foundation Shade Attribute Baseline

**Version:** 0.1  
**Status:** Initial implementation  
**Input source:** The Pudding makeup-shades CSV, pinned to upstream commit 3458c304647bef28ff2dd53f808bee3507f2a4f1.

## Purpose

This baseline ranks historical foundation product swatches against a user-supplied reference HEX colour using CIEDE2000 colour difference.

It is intentionally an **attribute-retrieval baseline**, not a trained recommender. It does not estimate a user's skin colour, assess actual foundation suitability, or predict preference or satisfaction. The reference colour can be any supplied swatch or test value. It must not be described as an actual person's skin tone unless separately measured under a justified, consented protocol.

## Data handling

- The CSV is fetched from a pinned raw GitHub URL at runtime.
- The source CSV is not copied into this repository or saved as part of the script output.
- The parser validates required fields and six-digit HEX swatches.
- Exact duplicate keys are defined by brand + product + HEX (case-insensitive HEX). The first source row is retained; duplicates are counted and reported.
- H/S/V missing values are counted as diagnostics only; they are not used for ranking.
- The disputed source L field is not read or used.

## Colour method

1. Parse the source and target HEX values as 8-bit sRGB.
2. Linearise encoded sRGB channels using the IEC 61966-2-1 transfer function.
3. Convert linear RGB to CIE XYZ using the sRGB/D65 matrix.
4. Convert XYZ to CIELAB using D65 and the 2-degree standard observer.
5. Rank product swatches by CIEDE2000 with kL = kC = kH = 1.

Lower CIEDE2000 distance means a smaller perceptual colour difference between the two represented swatches under the metric. It does not establish real-world appearance under different lighting, application, formulation, opacity, oxidation, skin surface, device calibration, or user preference.

## Reproducibility

- Upstream source revision is pinned; the script does not follow a moving branch.
- CIEDE2000 is tested against standard published reference pairs.
- Dataset parsing, duplicate handling, HEX validation, and ranking order have unit tests.
- GitHub Actions runs tests and one sample command on a GitHub-hosted runner.
- The project uses the Python standard library only for this baseline.

## Run

    python -m unittest discover -s tests -v
    python -m oge_fashion.shade_baseline --target-hex F3CFB3 --top-k 10

The second command needs an internet connection to fetch the pinned shade CSV. No dataset file is written locally.

## Source and licence

- Dataset README and collection method: https://github.com/the-pudding/data/blob/master/makeup-shades/README.md
- Pinned source CSV: https://raw.githubusercontent.com/the-pudding/data/3458c304647bef28ff2dd53f808bee3507f2a4f1/makeup-shades/shades.csv
- Upstream repository licence: https://github.com/the-pudding/data/blob/master/LICENSE
- CIEDE2000 reference method: Sharma, G., Wu, W., & Dalal, E. N. (2005), The CIEDE2000 color-difference formula: Implementation notes, supplementary test data, and mathematical observations, Color Research & Application, 30(1), 21–30. DOI: https://doi.org/10.1002/col.20070

The upstream repository contains a root-level MIT licence. Review the source repository's current licence and attribution conditions before redistributing the source CSV or derived data. This repository does not include that CSV.
