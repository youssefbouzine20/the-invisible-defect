# Youssef's data work

All 15 categories passed the integrity audit. The category notebooks show the inventory, mask overlays, and defect sizes. [Category notebooks](../notebooks/categories/)

## Next step

Bottle is ready with **167 training**, **42 validation**, and **83 official test** images. To prepare the other 14 categories, open the preparation notebook in VS Code, select `.venv`, and click **Run All**. Check the final counts and look for 15 files in `splits/`. [Bottle split](../splits/bottle.json) · [Preparation notebook](../notebooks/data_preparation.ipynb)

The shared code uses seed `42` to set aside about 20% of each category's normal training images for validation. Each category keeps its official test set. [Preparation code](../data_tools/preparation.py)

## Share with the team

After verifying the splits, share the project and point each teammate to their work folder. Bottle is the first model run. [Team guides](../README.md#who-does-what)

## When the model runs arrive

Collect the three run folders and compare the methods on their shared categories. [Handoff requirements](../README.md#what-to-hand-back) · [Evaluation plan](experiment_protocol.md)
