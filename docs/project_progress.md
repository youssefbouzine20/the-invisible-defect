# The Invisible Defect project progress

Updated 22 November 2026

The project compares CAE, VAE, and PatchCore on the original MVTec AD dataset. The goal is coverage of all 15 categories, starting with `bottle`. Each method fits a separate model or memory bank for each category and uses the same saved normal training split and official test images. Youssef prepares and analyzes the data first. Omar, Rime, and Houssam build the three models and return their predictions. Youssef then calculates the common metrics. [MVTec AD dataset page](https://www.mvtec.com/research-teaching/datasets/mvtec-ad)

## Work completed

| Milestone | Evidence |
| --- | --- |
| Repository started | The first GitHub commit added the README and `.gitignore`. [Initial GitHub commit](https://github.com/youssefbouzine20/the-invisible-defect/commit/283f3fac121c125002da51b2a95b4afcd4f10ac9) |
| Dataset acquisition | All 15 categories are available under `data/raw/mvtec-ad/`. The acquisition check counted 5,354 images and 1,258 ground-truth masks. The project copy matched the extracted source file by file using SHA-256. [MVTec benchmark, Table 1](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/05_research_teaching/datasets/mvtec_ad.pdf) |
| Audit environment | The Windows project environment uses Python 3.13.7. Audit dependencies are listed in [requirements.txt](../requirements.txt). Youssef confirmed that the VS Code notebook kernel uses the project's `.venv`. |
| Experiment protocol | The [experiment protocol](experiment_protocol.md) specifies the split, input and prediction formats, validation-based threshold, metrics, and benchmarking rules. |
| Bottle audit | The notebook inventory agreed with the script's folder counts. The saved report `outputs/audit/bottle.json` has status `PASS`. |
| Missing-mask test | A test fixture contained a defective image without its mask. The auditor identified the expected mask path and returned exit code `1`. |
| Full dataset audit | `outputs/audit/all.json` records `PASS` for all 15 categories, 1,258 matched image–mask pairs, and zero integrity issues. Every audited mask retained at least one marked pixel at 224 × 224. |
| Bottle analysis | The [bottle notebook](../notebooks/categories/bottle_audit.ipynb) reports the inventory, integrity checks, and defect sizes. The mask overlay for the selected `broken_small` example aligns with the chip on the lower-left rim. |
| Individual category notebooks | [The category notebook folder](../notebooks/categories/) contains one audit for each of the 15 categories. Saved runs for bottle, cable, capsule, carpet, grid, and hazelnut all show `PASS`, matching mask counts, two figures each, and zero errors. The other nine notebooks are ready for visual review. The [shared analysis code](../data_tools/audit_analysis.py) supplies the tables and figures for the 14 additional categories. |
| Bottle data prepared | The [bottle split](../splits/bottle.json) contains 167 training and 42 validation images. The official test set contains 83 images. The preparation preview resized `bottle/train/good/009.png` to 224 × 224. |
| All categories prepared | The [preparation notebook](../notebooks/data_preparation.ipynb) saved all 15 split files. The run showed **2,903 training**, **726 validation**, and **1,725 official test** images. The training and validation lists are disjoint within each category. |
| Team handoff | Shared scripts live in `data_tools/`. Each model folder has a short work guide. [Shared splits](../splits/) · [Team guides](../README.md#who-does-what) |

## Verified bottle results

The native bottle images and masks are 900 × 900 pixels. The counts below come from the local inventory and the saved audit report.

| Group | Training images | Official test images | Ground-truth masks |
| --- | ---: | ---: | ---: |
| Normal (`good`) | 209 | 20 | 0 |
| Large break (`broken_large`) | 0 | 20 | 20 |
| Small break (`broken_small`) | 0 | 22 | 22 |
| Contamination (`contamination`) | 0 | 21 | 21 |
| **Total** | **209** | **83** | **63** |

The audit matched all 63 defective test images by filename to their ground-truth masks. It found zero missing masks, zero unmatched masks, zero image or mask integrity issues, and zero exact pixel duplicate groups across the official training and test splits. All 63 masks retained at least one marked pixel when resized to 224 × 224 with nearest-neighbor interpolation. Use the native masks for localization scoring.

The saved notebook reports median mask areas of **2.4370%** for small breaks, **11.8670%** for large breaks, and **7.2479%** for contamination. The observed ranges overlap, so the planned size analysis should group defects by measured mask area.

## Reproduce the audit

From the project root in Git Bash, activate the environment and run the bottle audit:

```bash
source .venv/Scripts/activate
python data_tools/audit.py --root data/raw/mvtec-ad --category bottle
```

The audit script saves the inventory, integrity findings, and per-image mask measurements in `outputs/audit/bottle.json`. [Audit script](../data_tools/audit.py) · [Reference inventory](../data_tools/mvtec_ad_inventory.json) · [MVTec AD extended benchmark, Tables 1 and 8](https://link.springer.com/content/pdf/10.1007/s11263-020-01400-4.pdf)

The full audit command uses the same checks and saves a separate report at `outputs/audit/all.json`:

```bash
python data_tools/audit.py --root data/raw/mvtec-ad --all
```

## Decisions for the final report

- **Dataset.** Use the verified inventory and integrity checks across all 15 categories. Present the category-level size comparison and selected ground-truth overlays. Use the verified bottle figures to provide detailed context for the first model comparison.
- **Data preparation.** Save one split per category using seed `42` and about 20% of the category's normal training images for validation. Use the official test images and full-frame 224 × 224 RGB inputs.
- **Evaluation.** Compare image and pixel AUROC and average precision using the common evaluator. Fix each category's alert threshold using normal validation scores. Measure latency and memory with the same device and timing procedure across models. Report the categories completed by all three methods and their per-category results.

## Next steps

- [x] Audit all 15 categories and verify the bottle inventory, mask overlays, and defect-size results.
- [x] Verify the category notebooks for bottle, cable, capsule, carpet, grid, and hazelnut.
- [x] Save the shared split files for all 15 categories and prepare the team guides.
- [ ] Share the team guides and start with the bottle model runs.
- [ ] Collect the three frozen model run folders with predictions and heatmaps.
- [ ] Build and verify the common evaluator, then prepare the comparison tables and figures for the report.
- [ ] After reviewing the comparison and failure cases, choose and explore a future direction. Candidates include an inspection demo, a robustness study under different lighting, and an analysis of the costs of false alarms and missed defects.
