"""Tables and figures for individual MVTec AD category audits."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from PIL import Image


def load_category_audit(project_root: Path, category: str) -> tuple[Path, dict]:
    """Load one passing category record from the saved full audit."""
    report_path = project_root / "outputs" / "audit" / "all.json"
    if not report_path.is_file():
        raise FileNotFoundError(
            "Generate the full audit from the project root with "
            "python data_tools/audit.py --root data/raw/mvtec-ad --all"
        )

    audit = json.loads(report_path.read_text(encoding="utf-8"))
    category_reports = audit["categories"]
    if category not in category_reports:
        raise ValueError(f"Category {category!r} is missing from {report_path}.")

    report = category_reports[category]
    if report["status"] != "PASS":
        raise ValueError(f"Review the audit issues for {category!r} in {report_path}.")

    dataset_root = project_root / audit["dataset_root"]
    if not (dataset_root / category).is_dir():
        raise FileNotFoundError(f"Dataset category folder not found: {dataset_root / category}")
    return dataset_root, report


def inventory_table(report: dict) -> pd.DataFrame:
    """Show expected and actual PNG counts by folder."""
    return pd.DataFrame(report["inventory"]).rename(columns={
        "folder": "Folder",
        "expected": "Expected PNGs",
        "actual": "Actual PNGs",
    })


def integrity_table(report: dict) -> pd.DataFrame:
    """Summarize the image and mask checks in the saved audit."""
    width, height = report["resize_size"]
    return pd.DataFrame(
        [
            ("Matched image–mask pairs", report["matched_pairs"]),
            ("Missing masks", report["missing_masks"]),
            ("Masks without a matching image", report["unmatched_masks"]),
            ("Exact duplicate groups across train and test", report["cross_split_duplicate_groups"]),
            (f"Masks empty at {width} × {height}", report["masks_emptied_after_resize"]),
            ("Integrity issues", len(report["issues"])),
        ],
        columns=["Check", "Result"],
    )


def _display_name(name: str) -> str:
    return name.replace("_", " ").title()


def defect_size_summary(measurements: pd.DataFrame) -> pd.DataFrame:
    """Summarize each defect type's mask areas as percentages of its images."""
    return (
        measurements.groupby("defect_type", sort=True)["area_percent"]
        .agg(["count", "min", "median", "max"])
        .rename(index=_display_name, columns={
            "count": "Images",
            "min": "Minimum (%)",
            "median": "Median (%)",
            "max": "Maximum (%)",
        })
        .rename_axis("Defect type")
        .round(4)
    )


def plot_defect_sizes(measurements: pd.DataFrame, category: str) -> Figure:
    """Draw a log-scale boxplot of native mask areas by defect type."""
    groups = list(measurements.groupby("defect_type", sort=True)["area_percent"])
    figure, axis = plt.subplots(figsize=(8, 2 + 0.45 * len(groups)), layout="constrained")
    axis.boxplot(
        [areas for _, areas in groups],
        orientation="horizontal",
        tick_labels=[f"{_display_name(name)} (n={len(areas)})" for name, areas in groups],
        patch_artist=True,
        boxprops={"facecolor": "#cfe3f5", "edgecolor": "#275d86"},
        medianprops={"color": "#123951", "linewidth": 2},
    )
    axis.set_xscale("log")
    axis.set_xlabel("Defect mask area (% of original image, log scale)")
    axis.set_title(f"{_display_name(category)} defect sizes")
    axis.grid(axis="x", alpha=0.25)
    axis.invert_yaxis()
    return figure


def _load_overlay(dataset_root: Path, sample: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    image_path = dataset_root / sample["image_id"]
    mask_path = dataset_root / sample["mask_id"]
    with Image.open(image_path) as source:
        image = source.convert("RGB")
    with Image.open(mask_path) as source:
        mask = source.convert("L")

    if image.size != mask.size or mask.getbbox() is None:
        raise ValueError(f"The mask at {mask_path} no longer matches the saved audit.")

    preview = image.copy()
    preview.thumbnail((360, 360), Image.Resampling.LANCZOS)
    preview_mask = mask.resize(preview.size, Image.Resampling.NEAREST)
    if preview_mask.getbbox() is not None:
        image, mask = preview, preview_mask

    visible_mask = np.asarray(mask) > 0
    overlay = np.zeros((*visible_mask.shape, 4), dtype=np.uint8)
    overlay[visible_mask] = (242, 52, 47, 150)
    return np.asarray(image), overlay


def plot_mask_overlays(
    dataset_root: Path, measurements: pd.DataFrame, category: str
) -> Figure:
    """Show an original and a ground-truth overlay for each defect type."""
    groups = list(measurements.groupby("defect_type", sort=True))
    figure, axes = plt.subplots(
        len(groups), 2, figsize=(8, 2.8 * len(groups)), squeeze=False, layout="constrained"
    )
    for (defect_type, group), (original_axis, mask_axis) in zip(groups, axes):
        ordered = group.sort_values("image_id")
        areas = ordered["area_percent"]
        sample = ordered.iloc[(areas - areas.median()).abs().argmin()]
        image, overlay = _load_overlay(dataset_root, sample)

        original_axis.imshow(image)
        original_axis.set_title(f"{_display_name(defect_type)} · Original")
        mask_axis.imshow(image)
        mask_axis.imshow(overlay, interpolation="nearest")
        mask_axis.set_title(f"Ground truth · {sample['area_percent']:.3g}% of image")
        original_axis.axis("off")
        mask_axis.axis("off")

    figure.suptitle(f"MVTec AD {category.replace('_', ' ')} defect examples")
    return figure
