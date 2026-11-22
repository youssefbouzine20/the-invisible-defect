# Youssef's data work

The automated integrity audit passed for all 15 categories. The category notebooks show the inventory, mask overlays, and defect sizes. Saved visual runs have been reviewed for bottle, cable, capsule, carpet, grid, and hazelnut. [Category notebooks](../notebooks/categories/) · [Progress log](project_progress.md)

## What is ready

The saved preparation run produced all 15 split files in `splits/`. The totals are **2,903 training**, **726 validation**, and **1,725 official test** images. Bottle has **167 training**, **42 validation**, and **83 official test** images. [Bottle split](../splits/bottle.json) · [Preparation notebook](../notebooks/data_preparation.ipynb)

The shared code uses seed `42` to set aside about 20% of each category's normal training images for validation. Each category keeps its official test set. [Preparation code](../data_tools/preparation.py)

## Reproduce the notebooks

Once the dataset is in place, activate `.venv` and run these commands from the project root in Git Bash. [Setup](../README.md#setup)

```bash
source .venv/Scripts/activate
python data_tools/audit.py --root data/raw/mvtec-ad --category bottle
python data_tools/audit.py --root data/raw/mvtec-ad --all
```

The bottle notebook reads `outputs/audit/bottle.json`. The other category notebooks and the preparation notebook read `outputs/audit/all.json`. Select `.venv` as the notebook kernel in VS Code. For model work, use the committed split files directly. [Team guides](../README.md#who-does-what)

## When the model runs arrive

Collect the three run folders and compare the methods on their shared categories. [Handoff requirements](../README.md#what-to-hand-back) · [Evaluation plan](experiment_protocol.md)
