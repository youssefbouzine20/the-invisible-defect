# Omar — Convolutional autoencoder (CAE)

Build the CAE in `models/cae/`. Add your code and exact Git Bash commands for training and export in this folder.

## What Youssef prepared

- All 15 MVTec AD categories passed the data audit. Each category has a saved list of its normal training and validation images. [Category splits](../../splits/)
- Shared code loads those IDs and prepares full-frame RGB images at 224 × 224. [Setup](../../README.md#setup) · [Shared data example](../../README.md#use-the-shared-data)
- Bottle has **167 training**, **42 validation**, and **83 official test** images. Youssef will use the original ground-truth masks for localization evaluation. [Bottle split](../../splits/bottle.json)

## Your work

1. Start with bottle. Train the CAE to reconstruct the 167 normal training images. Use the 42 normal validation images to choose the settings and checkpoint.
2. Compare each image with its reconstruction to make an error heatmap. Decide how to combine its pixel errors into one anomaly score and record that rule. Keep the heatmap aligned with the full input image.
3. Freeze the model, preprocessing, and scoring rule. Export raw scores and heatmaps for all validation and official test images using those same settings.
4. Once the bottle export works, repeat with a separate CAE for each additional category you can complete. Use that category's saved split.

## What to return

Share one run folder under `outputs/cae/<run-id>/` with these files.

- **`predictions.csv`** with the header `sample_id,split,anomaly_score,map_path`. Bottle has **125 rows**, one for each of the 42 validation and 83 test images. Use the image ID relative to the dataset root and either `validation` or `test` as the split. Give more unusual images higher raw scores.
- **Heatmaps** with one finite `float32` NumPy `.npy` array of size 224 × 224 per row. Use a path relative to the run folder and include the category in each path.
- **`run.json`** with the method name, Git commit, library versions, and device. For each category, record the split version, seed, training settings, reconstruction loss, checkpoint filename, and scoring rule.

Include your implementation and run commands here. Share large checkpoints separately if needed. Youssef will use your raw predictions to calculate the common metrics. [Shared handoff format](../../README.md#what-to-hand-back)
