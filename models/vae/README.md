# Rime — Variational autoencoder

Put your VAE code in this folder. Start with bottle to get training and export working. Then repeat for the other categories as time and compute allow. [Shared data setup](../../README.md#setup)

1. Fit a separate VAE on each category’s normal training images. Read the train and validation IDs from `splits/<category>.json` and use the validation images to choose settings.
2. Define a repeatable way to score an image, such as reconstructing from the latent mean. Record the model, reconstruction loss, KL weight, and how you produce the heatmap and image score for each category in `run.json`.
3. Freeze the model and scoring rule before scoring that category’s official test images. Keep the heatmap aligned with the full 224 × 224 input.
4. Save one raw score and one heatmap per validation and test image for every completed category. Return one run folder under `outputs/vae/<run-id>/`. Youssef will compute the comparison metrics. [Shared handoff format](../../README.md#what-to-hand-back)
