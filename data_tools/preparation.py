"""Shared split and image preparation for MVTec AD categories."""

import json
import random
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

from .audit import INPUT_SIZE, REFERENCE_PATH


SEED = 42
MANIFEST_VERSION = 1


def _category_counts(category: str) -> dict:
    categories = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))["categories"]
    if category not in categories:
        raise ValueError(f"Unknown MVTec AD category: {category}")
    return categories[category]


def create_category_split(dataset_root: Path, category: str) -> dict:
    """Assign a category's official normal training images to train and validation."""
    expected_count = _category_counts(category)["train_good"]
    train_folder = dataset_root / category / "train" / "good"
    image_ids = sorted(
        path.relative_to(dataset_root).as_posix()
        for path in train_folder.glob("*.png")
        if path.is_file()
    )
    if len(image_ids) != expected_count:
        raise ValueError(
            f"Expected {expected_count} normal {category} images in {train_folder}. "
            f"Found {len(image_ids)}."
        )

    random.Random(SEED).shuffle(image_ids)
    validation_size = round(expected_count / 5)
    return {
        "version": MANIFEST_VERSION,
        "category": category,
        "seed": SEED,
        "train": image_ids[validation_size:],
        "validation": image_ids[:validation_size],
    }


def save_category_split(manifest_path: Path, manifest: dict) -> None:
    """Write a new manifest or confirm that the same split is already saved."""
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(manifest, indent=2) + "\n"

    try:
        stream = manifest_path.open("x", encoding="utf-8", newline="\n")
    except FileExistsError:
        if json.loads(manifest_path.read_text(encoding="utf-8")) != manifest:
            raise FileExistsError(
                f"A different split is already saved in {manifest_path}. Review it before changing it."
            ) from None
        return

    try:
        with stream:
            stream.write(text)
    except OSError:
        manifest_path.unlink(missing_ok=True)
        raise


def category_image_ids(
    dataset_root: Path, manifest_path: Path, category: str, split: str
) -> list[str]:
    """Read a category's saved split IDs or list its official test IDs."""
    if split == "test":
        counts = _category_counts(category)
        test_folder = dataset_root / category / "test"
        paths = [path for path in test_folder.glob("*/*.png") if path.is_file()]
        expected = {"good": counts["test_good"], **counts["defects"]}
        actual = Counter(path.parent.name for path in paths)
        if dict(actual) != expected:
            raise ValueError(
                f"Unexpected {category} test file counts in {test_folder}. "
                f"Expected {expected}, found {dict(sorted(actual.items()))}."
            )
        return sorted(path.relative_to(dataset_root).as_posix() for path in paths)

    if split not in ("train", "validation"):
        raise ValueError("Choose train, validation, or test.")

    if not manifest_path.is_file():
        raise FileNotFoundError(
            f"Split manifest missing at {manifest_path}. Run notebooks/data_preparation.ipynb to save it."
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest != create_category_split(dataset_root, category):
        raise ValueError(f"The split at {manifest_path} differs from the expected {category} split.")
    return manifest[split]


def create_bottle_split(dataset_root: Path) -> dict:
    """Build the bottle split using the shared preparation rule."""
    return create_category_split(dataset_root, "bottle")


def save_bottle_split(manifest_path: Path, manifest: dict) -> None:
    """Save a bottle split using the shared manifest writer."""
    save_category_split(manifest_path, manifest)


def bottle_image_ids(dataset_root: Path, manifest_path: Path, split: str) -> list[str]:
    """Read bottle image IDs using the shared split loader."""
    return category_image_ids(dataset_root, manifest_path, "bottle", split)


def prepare_image(image_path: Path) -> np.ndarray:
    """Resize the full RGB image and return channel-first float32 values in [0, 1]."""
    with Image.open(image_path) as original:
        resized = original.convert("RGB").resize(INPUT_SIZE, Image.Resampling.BILINEAR)
        pixels = np.asarray(resized, dtype=np.float32)
    return np.ascontiguousarray(pixels.transpose(2, 0, 1) / np.float32(255))
