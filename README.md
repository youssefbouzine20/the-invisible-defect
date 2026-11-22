# The Invisible Defect: Beyond Reconstruction

We compare three ways to detect defects using normal training images. Start with bottle, then extend to the remaining categories as time and compute allow. [MVTec AD dataset](https://www.mvtec.com/research-teaching/datasets/mvtec-ad)

## Who does what

| Person | Work folder and guide |
| --- | --- |
| Youssef | `data_tools/` and `notebooks/` for data preparation and analysis. [Data guide](docs/data_work.md) |
| Omar | `models/cae/` for the convolutional autoencoder. [CAE guide](models/cae/README.md) |
| Rime | `models/vae/` for the variational autoencoder. [VAE guide](models/vae/README.md) |
| Houssam | `models/patchcore/` for PatchCore. [PatchCore guide](models/patchcore/README.md) |

## Setup

Clone the repository in Git Bash and open the cloned folder in VS Code.

```bash
git clone https://github.com/youssefbouzine20/the-invisible-defect.git
cd the-invisible-defect
```

Download the original MVTec AD dataset from the link above. Extract it under `data/raw/mvtec-ad/` so the full path from the project root to the bottle training images is `data/raw/mvtec-ad/bottle/train/good/`. Use `python --version` in Git Bash to confirm it points to Python 3.13 before creating the shared data environment.

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Install the Python and Jupyter extensions in VS Code and select `.venv` as the notebook kernel. `requirements.txt` covers data exploration and preparation. Each model owner records their framework, package versions, and exact setup and run commands in their model folder. Keep the dataset, generated outputs, and environment local.

## Use the shared data

Start with `splits/bottle.json`, which lists 167 training and 42 validation images. All 15 split files are ready to use. Fit each model or memory bank on its category's training split and fix the settings before scoring the official test images. [Reproduce the audit and preparation notebooks](docs/data_work.md#reproduce-the-notebooks)

```python
from pathlib import Path

from data_tools.preparation import category_image_ids, prepare_image

dataset_root = Path("data/raw/mvtec-ad")
image_ids = category_image_ids(dataset_root, Path("splits/bottle.json"), "bottle", "train")
image = prepare_image(dataset_root / image_ids[0])
```

Run this from the project root. `prepare_image` returns the full image as 224 × 224 RGB with three channels first and values from 0 to 1. Use `"validation"` or `"test"` for the other lists. When your training script is ready, run it as a module from the project root so it can import `data_tools`. For example, if Omar creates `models/cae/train.py`, run `python -m models.cae.train`.

## What to hand back

Put the implementation and run commands in your assigned model folder on your Git branch. If you have read-only access, open a pull request from your fork. Share one local run folder under `outputs/<method>/<run-id>/` for the categories you completed separately from the Git branch.

| File | What it contains |
| --- | --- |
| `predictions.csv` | One row per validation or official test image. Use `sample_id`, `split`, `anomaly_score`, and `map_path`. The ID is the path relative to the dataset root, including its category. The split is `validation` or `test`. |
| Heatmap files | One 224 × 224 `float32` NumPy `.npy` file per row. Use category-specific paths relative to the run folder. Higher scores and values mean more unusual. |
| `run.json` | Model name, Git commit, package versions, and device. For each completed category, record the split version, settings, seed, and model or memory-bank filename. |

Return finite raw scores and heatmaps. Give Youssef the exact checkpoint or memory bank named in `run.json` so he can measure inference time and memory. It can travel with the run folder or be shared separately. Youssef will set thresholds and compare the methods once all three runs arrive. [Progress log](docs/project_progress.md) · [Evaluation plan](docs/experiment_protocol.md)
