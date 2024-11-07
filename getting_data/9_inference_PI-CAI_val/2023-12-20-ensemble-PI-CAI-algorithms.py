import argparse
import json
from pathlib import Path
from typing import List, Optional, Union

import numpy as np
import SimpleITK as sitk
from picai_prep import atomic_image_write
from tqdm import tqdm


def ensemble_case_level_predictions(
    prediction_dirs: List[Union[Path, str]],
    case_ids: Optional[List[str]] = None,
    output_dir: Optional[Union[Path, str]] = None,
) -> None:
    predictions = {}

    for prediction_dir in prediction_dirs:
        path = prediction_dir / "cspca-case-level-likelihood"
        if case_ids is None:
            case_ids = sorted([path.stem for path in path.glob("*.json")])

        for case_id in tqdm(case_ids, desc=prediction_dir.name):
            p = path / f"{case_id}.json"
            try:
                with open(p, encoding="utf-8") as f:  # Specify UTF-8 encoding
                    data = json.load(f)
            except UnicodeDecodeError:
                print(f"Warning: Could not decode {p}. Skipping this file.")
                continue
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON format in {p}. Skipping this file.")
                continue

            if case_id not in predictions:
                predictions[case_id] = []
            predictions[case_id].append(data)

    # Ensemble case-level predictions
    predictions_ensemble = {
        case_id: np.mean(case_predictions)
        for case_id, case_predictions in predictions.items()
    }

    # Save ensemble predictions
    if output_dir is None:
        output_dir = prediction_dirs[0].parent / "ensemble" / "cspca-case-level-likelihood"
    output_dir = Path(output_dir)
    path = output_dir / "predictions.json"
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(predictions_ensemble, f, indent=2)


def ensemble_voxel_level_predictions(
    prediction_dirs: List[Union[Path, str]],
    case_ids: Optional[List[str]] = None,
    output_dir: Optional[Union[Path, str]] = None,
) -> None:
    if case_ids is None:
        case_ids = sorted(
            [
                path.name.split(".nii.gz")[0]
                for path in Path(prediction_dirs[0] / "cspca-detection-map").glob("*.nii.gz")
            ]
        )
    if output_dir is None:
        output_dir = prediction_dirs[0].parent / "ensemble"
    output_dir = Path(output_dir) / "cspca-detection-map"

    for case_id in tqdm(case_ids):
        pred_ensemble = None
        ensemble_count = 0

        # ensemble voxel-level predictions
        for prediction_dir in prediction_dirs:
            pred_path = prediction_dir / "cspca-detection-map" / f"{case_id}.nii.gz"
            pred = sitk.ReadImage(str(pred_path))
            pred_arr = sitk.GetArrayFromImage(pred)
            if pred_ensemble is None:
                pred_ensemble = pred_arr
            else:
                pred_ensemble += pred_arr
            ensemble_count += 1

        pred_ensemble /= ensemble_count
        pred_ensemble = sitk.GetImageFromArray(pred_ensemble)
        pred_ensemble.CopyInformation(pred)

        # save
        path = output_dir / f"{case_id}.nii.gz"
        path.parent.mkdir(exist_ok=True, parents=True)
        atomic_image_write(pred_ensemble, path)


if __name__ == "__main__":
    # parse arguments and show defaults
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--prediction_dirs",
        type=Path,
        nargs="+",
        default=[
            Path("/data/pelvis/projects/joeran/picai/predictions/hidden_validation/DataScientX/"),
            Path("/data/pelvis/projects/joeran/picai/predictions/hidden_validation/HeviAI/"),
            Path("/data/pelvis/projects/joeran/picai/predictions/hidden_validation/PIMed/"),
            Path("/data/pelvis/projects/joeran/picai/predictions/hidden_validation/Swangeese/"),
            Path("/data/pelvis/projects/joeran/picai/predictions/hidden_validation/Z-SSMNet/"),
        ],
        help="List of directories containing the predictions.",
    )
    parser.add_argument(
        "--case_ids",
        nargs="+",
        default=None,
        help="List of case IDs to use. If None, all case IDs are used.",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=None,
        help="Directory to save the ensemble predictions to.",
    )
    args = parser.parse_args()

    # run
    ensemble_case_level_predictions(
        prediction_dirs=args.prediction_dirs,
        case_ids=args.case_ids,
        output_dir=args.output_dir,
    )
    ensemble_voxel_level_predictions(
        prediction_dirs=args.prediction_dirs,
        case_ids=args.case_ids,
        output_dir=args.output_dir,
    )
