# Cloud-First Development Workflow

## Goal
Keep laptop storage use close to zero. Source code, research notes, lightweight ontology files, and configurations live in GitHub. Large data and compute stay in cloud services where feasible.

## Recommended workflow
1. **GitHub:** source of truth for code, Markdown, ontology files, small fixtures, configuration templates, and reproducibility instructions.
2. **Browser IDE:** use GitHub Codespaces or another cloud IDE for editing and command-line work. Check availability, included quota, and billing before launch.
3. **Hosted notebooks:** use a cloud notebook for exploratory preparation and GPU experiments when its terms and storage fit the dataset licence.
4. **Object storage:** keep approved large datasets and checkpoints outside Git; store only manifests, permissible checksums, and access instructions in the repository.
5. **GitHub Actions:** run lightweight linting, ontology parse checks, tests, and documentation validation; do not treat CI as a GPU compute substitute.

## Storage rules
- Do not clone large datasets to the laptop.
- Do not commit datasets, checkpoints, generated image collections, or secrets.
- Add large/restricted patterns to `.gitignore` before implementation.
- Check Git LFS quotas before using it; it is not unlimited storage.
- Prefer small synthetic fixtures for tests.
- Delete cloud resources and temporary copies when no longer required.

## Security and privacy
- Store credentials in secret managers or Codespaces secrets, never source files.
- Use least-privilege credentials.
- Do not upload participant data or face images to third-party services without an approved legal/ethical basis and participant notice/consent.
- Separate research-only data from public-product data.
- Record data region, retention, access, and deletion steps for cloud services holding personal data.

## Cost controls
- Start with CPU and tiny synthetic data for ontology development.
- Use GPU only after a specific model requirement is established.
- Set budgets/alerts where available.
- Stop idle runtimes and delete unused disks, buckets, and snapshots.
- Record runtime/hardware for reported experiments.

## First cloud setup checklist
- [ ] Confirm browser IDE availability and understand quota/billing.
- [ ] Open repository in browser IDE.
- [ ] Verify Markdown, Turtle, and small Python workflow.
- [ ] Add `.gitignore` for Python caches, notebooks, secrets, data directories, and model artefacts.
- [ ] Create a small synthetic fixture.
- [ ] Run and document an RDF/OWL parse check.

## Limitation
Cloud-first development avoids local storage pressure but does not remove dataset licence obligations, cloud costs, transfer costs, provider quotas, or privacy responsibilities.
