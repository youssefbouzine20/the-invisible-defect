# Rime — Variational autoencoder (VAE)

Build the VAE and put your code and Git Bash run commands in this folder. Get the full workflow working for bottle first.

## What Youssef prepared

- Youssef audited all 15 MVTec AD categories and saved the normal training and validation image IDs for each one. The bottle split contains 167 training images and 42 validation images. [Bottle split](../../splits/bottle.json) · [All splits](../../splits/)
- The shared `category_image_ids` and `prepare_image` functions load the IDs and resize the full image to 224 × 224 RGB. The model input has shape `(3, 224, 224)` with values between 0 and 1. [Setup](../../README.md#setup) · [Shared data example](../../README.md#use-the-shared-data)
- The official bottle test set contains 83 images. Youssef will use the original pixel masks to evaluate where the model finds defects. [Data work](../../docs/data_work.md)

## Your work

1. Train the VAE on the 167 normal bottle training images. Record the architecture, reconstruction loss, KL weight, and training settings. Use the 42 normal validation images to choose settings and select the checkpoint.
2. Define how to score each image and pixel from its reconstruction. At inference, you can decode the latent mean for a repeatable reconstruction. If you sample instead, record the seeds, number of samples, and how you combine them. Record how you turn the heatmap into a single image score.
3. Freeze the checkpoint, preprocessing, and scoring rules before running on the official test images. Apply the same rules to validation and test and keep each heatmap aligned with the full input image.
4. When bottle training and export work, fit a fresh VAE for each additional category you can complete, using that category's saved splits.

## What to return

Share one local run folder under `outputs/vae/<run-id>/` containing the following files.

- `predictions.csv` with the header `sample_id,split,anomaly_score,map_path`. For bottle, include 125 rows, one for each of the 42 validation and 83 test images. Use image IDs relative to the dataset root, such as `bottle/test/broken_small/000.png`, and the split values `validation` and `test`.
- One finite 224 × 224 `float32` NumPy `.npy` heatmap for each row. Use `map_path` values relative to the run folder and include the category in the path. Raw image scores and heatmap values should be finite, with larger values meaning more unusual.
- `run.json` with the model name, Git commit, library versions, and device. For each completed category, include the split version, seed, checkpoint filename, training settings, and exact scoring rules. Share the checkpoint separately if needed to rerun the model.

Add the exact setup, training, and prediction export commands here when the code is ready. Youssef will evaluate the exported scores and maps. [Shared handoff format](../../README.md#what-to-hand-back)
