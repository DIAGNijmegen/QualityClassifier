import os
import random
import shutil
import json
from pathlib import Path
import SimpleITK as sitk  # For converting .mha to .nii.gz
from utils.utils import load_seed

if __name__ == '__main__':
    # Paths
    mountpoint = Path('/Volumes')
    raw_data_path = mountpoint / 'pelvis/projects/tiago/DWI_IQA/data/raw'
    nnunet_raw_data_path = raw_data_path / 'nnUnet_raw_data'

    # Check if LQ and HQ folders exist and are not empty
    lq_path = raw_data_path / 'LQ'
    hq_path = raw_data_path / 'HQ2'
    print("Checking if LQ and HQ folders exist and are not empty...")
    if not lq_path.exists() or not hq_path.exists():
        print("Error: LQ and/or HQ folders do not exist.")
        exit(1)
    if not any(lq_path.iterdir()) or not any(hq_path.iterdir()):
        print("Error: LQ and/or HQ folders are empty.")
        exit(1)
    print("LQ and HQ folders are verified and ready.")

    # Create nnUnet_raw_data and Task folder
    nnunet_raw_data_path.mkdir(parents=True, exist_ok=True)
    task_name = 'ProstateQualityDWI' # input("Enter the Task Name: ")
    task_folder_name = f'Task001_{task_name}'
    task_folder_path = nnunet_raw_data_path / task_folder_name
    task_folder_path.mkdir(parents=True, exist_ok=True)
    images_tr_path = task_folder_path / 'imagesTr'
    images_tr_path.mkdir(parents=True, exist_ok=True)

    print(f"Task folder '{task_folder_name}' and 'imagesTr' subfolder created.")

    print("Warning: All images will be 100% converted to training, with no test images.")
    if input("Do you want to proceed? (yes/no): ").strip().lower() != 'yes':
        print("Process aborted.")
        exit(1)

    # Only include valid .mha files, excluding files that start with ._
    all_images = [(img, 0) for img in lq_path.glob('*.mha') if not img.name.startswith('._')] + \
                 [(img, 1) for img in hq_path.glob('*.mha') if not img.name.startswith('._')]
    print(f"Found {len(all_images)} images (combined from LQ and HQ) for processing.")

    # Set seed and shuffle
    seed = load_seed()
    print(f"Using seed {seed} for shuffling images.")
    random.seed(seed)
    random.shuffle(all_images)
    print("Images shuffled.")

    correspondence = {}
    print("Converting images from .mha to .nii.gz format and renaming...")
    for idx, (img_path, quality) in enumerate(all_images, start=1):
        new_name = f"{task_name}_{idx:04d}_0000.nii.gz"
        output_path = images_tr_path / new_name
        # Convert from .mha to .nii.gz

        try:
            image = sitk.ReadImage(str(img_path))
            sitk.WriteImage(image, str(output_path))
            print(f"Converted and saved: {img_path.name} -> {new_name}")
        except Exception as e:
            print(f"Failed to convert {img_path.name}: {e}")

        # Record correspondence
        correspondence[img_path.name] = new_name

    # Save correspondence.json
    correspondence_path = task_folder_path / 'correspondence.json'
    with open(correspondence_path, 'w') as f:
        json.dump(correspondence, f, indent=4)
    print("Saved correspondence.json with original and new file names.")

    # Prepare dataset.json structure
    dataset = {
        "name": task_name,
        "description": "Dataset for prostate quality assessment.",
        "reference": "Unknown",
        "licence": "Unknown",
        "release": "1.0",
        "tensorImageSize": "3D",
        "modality": {"0": "MRI"},
        "classification_labels": [
            {
                "name": "Quality",
                "ordinal": False,
                "values": {
                    "0": "Low Quality",
                    "1": "High Quality"
                }
            }
        ],
        "training": [],
        "test": []
    }

    # Populate the training list in dataset.json
    print("Populating training list in dataset.json...")
    for idx, (img_path, quality) in enumerate(all_images, start=1):
        img_name = f"{task_name}_{idx:04d}_0000.nii.gz"
        dataset["training"].append({
            "image": f"./imagesTr/{img_name}",
            "Quality": quality
        })
    print(f"Added {len(dataset['training'])} entries to the training list in dataset.json.")

    # Save dataset.json
    dataset_path = task_folder_path / 'dataset.json'
    with open(dataset_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    print("Saved dataset.json with dataset structure and training images.")

    print("Process complete. Check the Task folder for the generated dataset.")
