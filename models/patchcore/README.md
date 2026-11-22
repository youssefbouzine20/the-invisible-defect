# Houssam — PatchCore

Put your PatchCore code in this folder. Start with bottle to get the memory bank and export working. Then repeat for the other categories as time and compute allow. [Shared data setup](../../README.md#setup)

1. Keep the pretrained feature extractor frozen. For each category, build a separate memory bank from its normal training IDs in `splits/<category>.json`. Use that category’s normal validation IDs to choose settings.
2. Record the memory bank, pretrained weights, feature layers, number of patches kept, and how patch distances become a heatmap and image score for each category in `run.json`.
3. Freeze the memory bank and scoring rule before scoring that category’s official test images. Align the heatmap with the full 224 × 224 input.
4. Save one raw score and one heatmap per validation and test image for every completed category. Return one run folder under `outputs/patchcore/<run-id>/`. Youssef will compute the comparison metrics. [Shared handoff format](../../README.md#what-to-hand-back)
