# Houssam — PatchCore

Build PatchCore in `models/patchcore/`. Add your code and the commands to reproduce your run in this folder.

## What Youssef prepared

- The dataset audit passed for all 15 categories. Each category has saved normal training and validation image lists. [Category splits](../../splits/)
- The shared loader reads those IDs and prepares full-frame RGB images at 224 × 224. The original test images and masks are ready for evaluation. [Setup](../../README.md#setup) · [Shared image preparation](../../README.md#use-the-shared-data)
- Bottle has **167 training**, **42 validation**, and **83 official test** images. [Bottle split](../../splits/bottle.json)

## Your work

1. Start with bottle. Use a frozen pretrained feature extractor to collect features from normal training patches. Store the selected patch features in a memory bank.
2. Use normal validation images to choose settings. Decide how the distance from the memory bank becomes a heatmap and a single image score. Keep maps aligned with the full 224 × 224 image.
3. Freeze the memory bank and scoring rule. Export raw scores and heatmaps for all validation and official test images.
4. Once the bottle export works, repeat the process with a separate memory bank for each additional category you complete.

## What to return

Share one run folder under `outputs/patchcore/<run-id>/` with these files.

- **`predictions.csv`** with the header `sample_id,split,anomaly_score,map_path`. Bottle has **125 rows**, one for each of the 42 validation and 83 test images. Use the image ID relative to the dataset root and either `validation` or `test` as the split. Give more unusual images higher raw scores.
- **Heatmaps** with one finite `float32` NumPy `.npy` array of size 224 × 224 per row. Use a path relative to the run folder and include the category in each path.
- **`run.json`** with the method name, Git commit, library versions, and device. For each category, record the split version, seed, pretrained weights, feature layers, patch selection, memory bank filename, and scoring rule.

Include your implementation and run commands here. Share large memory bank files separately if needed. Youssef will use your raw predictions to calculate the common metrics. [Shared handoff format](../../README.md#what-to-hand-back)
