# Youssef's data work

All 15 categories passed the integrity audit. The category notebooks show the inventory, mask overlays, and defect sizes. [Category notebooks](../notebooks/categories/)

## Next step

The saved preparation run produced all 15 split files in `splits/`. The totals are **2,903 training**, **726 validation**, and **1,725 official test** images. Bottle has **167 training**, **42 validation**, and **83 official test** images. [Bottle split](../splits/bottle.json) · [Preparation notebook](../notebooks/data_preparation.ipynb)

The shared code uses seed `42` to set aside about 20% of each category's normal training images for validation. Each category keeps its official test set. [Preparation code](../data_tools/preparation.py)

## Share with the team

After verifying the splits, share the project and point each teammate to their work folder. Bottle is the first model run. [Team guides](../README.md#who-does-what)

## When the model runs arrive

Collect the three run folders and compare the methods on their shared categories. [Handoff requirements](../README.md#what-to-hand-back) · [Evaluation plan](experiment_protocol.md)
