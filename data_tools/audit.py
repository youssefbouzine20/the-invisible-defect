"""Audit images and masks from the original MVTec AD dataset."""

import argparse
import json
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image


DEFAULT_CATEGORY = "bottle"
INPUT_SIZE = (224, 224)
REFERENCE_PATH = Path(__file__).with_name("mvtec_ad_inventory.json")


def audit_category(dataset_root: Path, category: str, reference: dict) -> dict:
    """Return inventory, integrity findings, and measurements for valid pairs."""
    category_root = dataset_root / category
    expected_counts = {
        "train/good": reference["train_good"],
        "test/good": reference["test_good"],
    }
    for defect, count in reference["defects"].items():
        expected_counts[f"test/{defect}"] = count
        expected_counts[f"ground_truth/{defect}"] = count

    files = {
        path.relative_to(category_root).as_posix(): path
        for path in sorted(category_root.rglob("*.png"))
        if path.is_file()
    }
    folder_counts = Counter(
        path.parent.relative_to(category_root).as_posix() for path in files.values()
    )
    inventory = [
        {
            "folder": folder,
            "expected": expected_counts.get(folder, 0),
            "actual": folder_counts[folder],
        }
        for folder in sorted(expected_counts.keys() | folder_counts.keys())
    ]
    issues = []
    if not category_root.is_dir():
        issues.append(f"Missing category directory: {category_root}")
    for row in inventory:
        if row["actual"] != row["expected"]:
            issues.append(
                f"{category}/{row['folder']}: expected {row['expected']} PNG files, found {row['actual']}"
            )

    expected_masks = {
        f"ground_truth/{path.parent.name}/{path.stem}_mask.png": name
        for name, path in files.items()
        if path.parent.parent == category_root / "test" and path.parent.name != "good"
    }
    actual_masks = {name for name in files if name.startswith("ground_truth/")}
    matched_masks = sorted(expected_masks.keys() & actual_masks)
    missing_masks = sorted(expected_masks.keys() - actual_masks)
    unmatched_masks = sorted(actual_masks - expected_masks.keys())
    for name in missing_masks:
        issues.append(f"{category}/{expected_masks[name]}: missing {category}/{name}")
    for name in unmatched_masks:
        issues.append(f"{category}/{name}: mask without a matching test image")

    sizes = {}
    mask_stats = {}
    fingerprints = {"train": defaultdict(list), "test": defaultdict(list)}
    for name, path in files.items():
        split = name.split("/", 1)[0]
        try:
            with Image.open(path) as image:
                image.load()
                sizes[name] = image.size
                if split == "ground_truth":
                    grayscale = image.convert("L")
                    total_pixels = image.width * image.height
                    defect_pixels = total_pixels - grayscale.histogram()[0]
                    resized = grayscale.resize(INPUT_SIZE, Image.Resampling.NEAREST)
                    mask_stats[name] = {
                        "defect_pixels": defect_pixels,
                        "area_percent": 100 * defect_pixels / total_pixels,
                        "empty_after_resize": resized.getbbox() is None,
                    }
                    if defect_pixels == 0:
                        issues.append(f"{category}/{name}: empty defect mask")
                elif split in fingerprints:
                    rgb = image.convert("RGB")
                    fingerprint = (rgb.size, sha256(rgb.tobytes()).hexdigest())
                    fingerprints[split][fingerprint].append(f"{category}/{name}")
        except (OSError, ValueError) as error:
            issues.append(f"{category}/{name}: could not read the PNG ({error})")

    measurements = []
    for mask_name in matched_masks:
        image_name = expected_masks[mask_name]
        if mask_name not in mask_stats or image_name not in sizes:
            continue
        if sizes[mask_name] != sizes[image_name]:
            issues.append(
                f"{category}/{mask_name}: mask size {sizes[mask_name]} differs from "
                f"image size {sizes[image_name]} for {category}/{image_name}"
            )
            continue
        stats = mask_stats[mask_name]
        if stats["defect_pixels"] > 0:
            measurements.append({
                "image_id": f"{category}/{image_name}",
                "mask_id": f"{category}/{mask_name}",
                "defect_type": files[mask_name].parent.name,
                **stats,
            })

    shared_fingerprints = fingerprints["train"].keys() & fingerprints["test"].keys()
    for fingerprint in sorted(shared_fingerprints):
        paths = fingerprints["train"][fingerprint] + fingerprints["test"][fingerprint]
        issues.append(f"Exact pixel duplicate across train and test: {', '.join(paths)}")

    return {
        "category": category,
        "dataset_root": dataset_root.as_posix(),
        "status": "FAIL" if issues else "PASS",
        "inventory": inventory,
        "matched_pairs": len(matched_masks),
        "missing_masks": len(missing_masks),
        "unmatched_masks": len(unmatched_masks),
        "cross_split_duplicate_groups": len(shared_fingerprints),
        "resize_size": list(INPUT_SIZE),
        "masks_emptied_after_resize": sum(row["empty_after_resize"] for row in measurements),
        "mask_measurements": measurements,
        "issues": issues,
    }


def write_report(report: dict, output: Path) -> None:
    """Replace the report after the new file has been written completely."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as directory:
        temporary_path = Path(directory) / output.name
        temporary_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        temporary_path.replace(output)


def print_category_report(report: dict) -> None:
    name = report["category"].replace("_", " ").capitalize()
    print(f"{name} audit: {report['status']}")
    for row in report["inventory"]:
        print(f"  {row['folder']:<26} {row['actual']:>3} / {row['expected']:>3} expected")
    print(f"Matched image-mask filenames: {report['matched_pairs']}")
    print(f"Missing masks: {report['missing_masks']}")
    print(f"Unmatched masks: {report['unmatched_masks']}")
    print(f"Exact duplicate groups across train and test: {report['cross_split_duplicate_groups']}")
    print(f"Masks that became empty at 224 x 224: {report['masks_emptied_after_resize']}")
    print(f"Integrity issues: {len(report['issues'])}")
    for issue in report["issues"]:
        print(f"  - {issue}")


def main() -> int:
    references = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))["categories"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Directory containing the category folders")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--category", choices=sorted(references), help="Category to audit (default: bottle)")
    selection.add_argument("--all", action="store_true", help="Audit all 15 categories")
    parser.add_argument("--output", type=Path, help="Path to the generated JSON report")
    args = parser.parse_args()

    if args.all:
        categories = {}
        for category in sorted(references):
            result = audit_category(args.root, category, references[category])
            categories[category] = result
            print(
                f"{category}: {result['status']} | {result['matched_pairs']} pairs | "
                f"{len(result['issues'])} integrity issues",
                flush=True,
            )
            for issue in result["issues"]:
                print(f"  - {issue}")

        passed = sum(result["status"] == "PASS" for result in categories.values())
        report = {
            "dataset_root": args.root.as_posix(),
            "status": "PASS" if passed == len(categories) else "FAIL",
            "categories_checked": len(categories),
            "categories_passed": passed,
            "matched_pairs": sum(result["matched_pairs"] for result in categories.values()),
            "integrity_issues": sum(len(result["issues"]) for result in categories.values()),
            "categories": categories,
        }
        output = args.output or Path("outputs/audit/all.json")
        write_report(report, output)
        print(f"Full audit: {report['status']} ({passed}/{len(categories)} categories passed)")
        print(f"Matched image-mask filenames: {report['matched_pairs']}")
        print(f"Integrity issues: {report['integrity_issues']}")
    else:
        category = args.category or DEFAULT_CATEGORY
        report = audit_category(args.root, category, references[category])
        output = args.output or Path(f"outputs/audit/{category}.json")
        write_report(report, output)
        print_category_report(report)

    print(f"JSON report: {output}")
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
