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
| Bottle audit | The notebook inventory agreed with the script's folder counts. Youssef ran the audit in Git Bash and saved `outputs/audit/bottle.json` with status `PASS`. |
| Missing-mask test | Youssef ran a temporary example containing a defective image without its mask. The auditor identified the expected mask path and returned exit code `1`. |
| Full dataset audit | `outputs/audit/all.json` records `PASS` for all 15 categories, 1,258 matched image–mask pairs, and zero integrity issues. Every audited mask retained at least one marked pixel at 224 × 224. |
| First notebook overlay | The side-by-side figure from `notebooks/categories/bottle_audit.ipynb` shows one `broken_small` test image. In Youssef's screenshot, the red ground-truth mask aligns with the visible chip on the lower-left rim. |
| Completed audit notebook | The notebook uses `outputs/audit/bottle.json` for the inventory, integrity table, and defect sizes. The saved VS Code run shows `PASS`, a three-type overlay figure, and a defect-area plot and summary table. All four code cells have saved execution counts and no error outputs. |
| Individual category notebooks | [The category notebook folder](../notebooks/categories/) contains one audit for each of the 15 categories. Saved runs for bottle, cable, capsule, carpet, grid, and hazelnut all show `PASS`, matching mask counts, two figures each, and zero errors. The other nine notebooks are ready for visual review. The [shared analysis code](../data_tools/audit_analysis.py) supplies the tables and figures for the 14 additional categories. |
| Notebook structure cleanup | Moved the combined overview to the local Git-ignored archive at `outputs/archived_notebooks/mvtec_ad_analysis.ipynb`. The active notebook folder groups individual audits under `notebooks/categories/`. |
| Bottle data prepared | The saved bottle run shows `PASS`, seed `42`, 167 training images, 42 validation images, and 83 official test images. It prepared `bottle/train/good/009.png` at 224 × 224 and saved the [bottle split](../splits/bottle.json). The run with its original outputs is in `outputs/archived_notebooks/bottle_data_preparation.ipynb`. |
| Preparation extended to all categories | The updated [preparation notebook](../notebooks/data_preparation.ipynb) and [shared code](../data_tools/preparation.py) create one split per category. The expected totals are 2,903 training, 726 validation, and 1,725 official test images. The original bottle split was verified by SHA-256. Youssef's run to write the other 14 files is pending. |
| Compact team layout | Shared scripts live in `data_tools/`. The three work folders have their own README under `models/`. The seven notebooks with saved outputs were backed up under Git-ignored `outputs/local_notebook_runs/` before the active notebooks were cleared for sharing. [Team guides](../README.md#who-does-what) |

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

- [x] Run `--all` in Git Bash and review the saved full-audit summary.
- [x] Load `bottle.json` in [the bottle notebook](../notebooks/categories/bottle_audit.ipynb) and visually check the first mask overlay.
- [x] Consolidate the bottle notebook around the saved audit report and add the final overlay and defect-size cells.
- [x] Review the saved notebook run, including both figures and the defect-size table.
- [x] Verify the individual notebook workflow using saved runs for bottle, cable, capsule, carpet, grid, and hazelnut.
- [x] Build the shared split and image preparation code, organize the team folders, and write the four work guides.
- [x] Verify the original bottle preparation run and its split file.
- [ ] Run the updated [data preparation notebook](../notebooks/data_preparation.ipynb), verify the per-category counts and totals, and confirm that all 15 split files exist.
- [ ] Share the remaining split files and point each teammate to their model folder.
- [ ] Collect the three frozen model run folders with predictions and heatmaps.
- [ ] Build and verify the common evaluator, then prepare the comparison tables and figures for the report.
- [ ] After reviewing the comparison and failure cases, choose and explore a future direction. Candidates include an inspection demo, a robustness study under different lighting, and an analysis of the costs of false alarms and missed defects.

The [project workflow](../AGENTS.md) keeps this log current as work is completed and results are verified.
