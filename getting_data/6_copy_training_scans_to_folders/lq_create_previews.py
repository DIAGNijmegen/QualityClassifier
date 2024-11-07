#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk

def plot_preview(subject_id: str, scan_path: Path, preview_save_dir: Path, comment: str) -> str:
    save_path = preview_save_dir / f"{subject_id}.png"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    if save_path.exists():
        return f"NOTE: Skipping - Preview Already Exists {save_path}"

    try:
        # Load the HBV scan
        img = sitk.GetArrayFromImage(sitk.ReadImage(str(scan_path)))

        # Set up the figure for plotting
        f, axes2d = plt.subplots(1, 3, figsize=(18, 6), squeeze=False)
        f.suptitle(comment, fontsize=16)

        # Plot the middle slice for each axis
        mid_slice_x = img.shape[0] // 2
        mid_slice_y = img.shape[1] // 2
        mid_slice_z = img.shape[2] // 2

        axes2d[0, 0].imshow(img[mid_slice_x, :, :], cmap="gray")
        axes2d[0, 1].imshow(np.flip(img[:, mid_slice_y, :], 0), cmap="gray")
        axes2d[0, 2].imshow(np.flip(img[:, :, mid_slice_z], 0), cmap="gray")

        # Save the figure
        f.savefig(save_path)
        plt.close(f)
    except Exception as e:
        return f"ERROR: Image Cannot Be Plotted {subject_id}: {e}"

def main():
    # Path to the folder containing HBV scans
    hbv_folder = Path("/Volumes/pelvis/projects/tiago/DWI_IQA/data/raw/HQ")
    # Path to save preview images
    preview_save_dir = hbv_folder / "previews"
    # Placeholder list for subject IDs and comments (could be filenames)
    hbv_files = [file for file in hbv_folder.glob("*.mha")]

    for hbv_file in hbv_files:
        subject_id = hbv_file.stem  # Using file name (without extension) as subject ID
        comment = f"Preview for {subject_id}"
        plot_preview(subject_id, hbv_file, preview_save_dir, comment)

if __name__ == "__main__":
    main()