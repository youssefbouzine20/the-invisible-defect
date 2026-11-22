# MVTec AD experiment protocol

The project compares CAE, VAE, and PatchCore on the original MVTec AD dataset. Start with `bottle`, then aim to cover all 15 categories. Each method fits a separate model or memory bank per category using the same normal training images as the other methods. Record the source of any pretrained weights, including PatchCore's backbone. [MVTec dataset paper, Table 1](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/05_research_teaching/datasets/mvtec_ad.pdf), [PatchCore paper](https://openaccess.thecvf.com/content/CVPR2022/html/Roth_Towards_Total_Recall_in_Industrial_Anomaly_Detection_CVPR_2022_paper.html)

## Dataset splits

| Split | Bottle example | Use |
| --- | ---: | --- |
| Project training | 167 normal | Fit model parameters, preprocessing statistics, or the PatchCore memory bank |
| Project validation | 42 normal | Check model behavior on unseen normal images, select eligible settings, and calibrate the image threshold |
| Official test | 20 normal and 63 defective | Evaluate the frozen runs on image-level detection and defect localization |

Create the training and validation sets from each category's official `train/good/` directory. Sort the dataset-relative image IDs and shuffle with Python's `random.Random(42)`. Use the first 20% for validation, rounded to the nearest image, and the rest for training. Commit one split file per category under `splits/`. Use `/` as the path separator in every ID, such as `bottle/train/good/000.png`.

Use the test directory and its masks for data integrity checks, descriptive exploration, and final evaluation. Base model selection, score processing, and calibration on normal training and validation images or predeclared settings. Freeze preprocessing, the checkpoint or memory bank, and the score rule before exporting predictions on the official test set. Set the image threshold using the exported normal validation scores before reporting test metrics.

## Images and predictions

Convert images to RGB and resize the full frame to 224 × 224 with antialiased bilinear interpolation. The shared preparation function returns channel-first NumPy `float32` arrays with shape `(3, 224, 224)` and values in `[0, 1]`. Convert the arrays to the model framework's input format in the model adapter. Apply any additional normalization there and keep all exported maps aligned with the full frame.

Keep the native binary masks for evaluation. Defective test images use their matching `ground_truth/` PNG. Normal test images use an all-zero mask at the original image size. Use nearest-neighbor interpolation when a binary mask needs resizing for a diagnostic.

Each run supplies a `predictions.csv` with one row per validation or test image for each completed category. The columns are `sample_id`, `split`, `anomaly_score`, and `map_path`. Use `validation` and `test` as the split values. Each `map_path` is relative to the run directory and points to a NumPy `.npy` array with shape `(224, 224)` and dtype `float32`. Export finite, unthresholded scores with larger values indicating more anomalous images or pixels. Treat image IDs as identifiers for joining predictions to ground truth. Use the same scoring and map processing for both splits of a category.

Store the outputs under `outputs/<method>/<run-id>/`. Include `run.json` with the model name, Git commit, library versions, and device. List the completed categories and record the split version, settings, seed, and checkpoint or memory bank identifier for each. Youssef will calibrate thresholds and evaluate the three runs after their outputs arrive.

## Image and pixel metrics

- **Image detection.** Compute AUROC and average precision on the official test image scores for each category. Choose each model's threshold for a category using that category's normal validation scores. For bottle, sort the 42 validation scores and use the 41st as the threshold. Set the threshold rule for the other categories before evaluating the models. Classify a test image as defective when its score is strictly above the threshold. Report the confusion matrix, precision, recall, F1, and observed false alarms. Mark precision as undefined if the number of predicted defects is zero. [AUROC definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html), [Average precision definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html)
- **Localization.** Bilinearly upsample each continuous anomaly map to the native image size. Compute pixel AUROC and pixel average precision by pooling aligned predictions and masks within each category's official test split, including normal images.
- **Failure analysis.** Review false alarms on normal images and report detected versus total images by defect type and mask area. Measure area as the percentage of native image pixels marked defective. Use bands of less than 0.1%, 0.1% to less than 1%, and 1% or greater. Report median per-image pixel average precision for each band with at least one defective image. Show the same images when comparing heatmaps across methods.

Compare the methods on the categories all three completed. Report the per-category results and give each shared category equal weight in the average.

## Runtime and memory

Benchmark all methods on the same machine and device with the same precision and batch size one. For each category, warm up with the first 10 validation images in its split file. Then time three passes over that category's official test images in the same fixed order. Start with the prepared input in CPU memory and stop when the image score and heatmap are available in CPU memory. Run file reading, plotting, and result export outside the timed interval. Synchronize CUDA before starting and stopping a GPU timer. [PyTorch CUDA synchronization](https://docs.pytorch.org/docs/2.12/generated/torch.cuda.synchronize.html)

Report median and 95th-percentile latency in milliseconds per image. Use a fresh process for each method to measure peak process RAM, and record peak PyTorch-allocated GPU memory separately when applicable. Include the device and measurement method with the reported values. [PyTorch CUDA memory statistic](https://docs.pytorch.org/docs/2.12/generated/torch.cuda.memory.max_memory_allocated.html)

## Checks before final evaluation

1. Confirm that the training and validation IDs are disjoint and together cover the official normal training files.
2. Check that each export contains exactly one row and one finite score map per expected image. Reject missing IDs, duplicates, unknown IDs, and invalid maps.
3. Check known-answer examples for ranking metrics, exact threshold ties, and score-map alignment before evaluating frozen model runs.
