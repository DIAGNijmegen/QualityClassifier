import SimpleITK as sitk
from pathlib import Path


def convert_to_prostate_quality_format(input_file, output_folder, sequence_number=764):
    input_file = Path(input_file)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)  # Ensure the output folder exists

    # Define the output file name
    output_file = output_folder / f"ProstateQualityDWI_{sequence_number:04d}_0000.nii.gz"
    print(input_file.exists())
    try:
        # Read the input image
        image = sitk.ReadImage(str(input_file))

        # Save the image in the specified output format and location
        sitk.WriteImage(image, str(output_file))

        print(f"Converted and saved as: {output_file}")
    except Exception as e:
        print(f"Failed to convert {input_file.name}: {e}")

# Example usage input_file='/Volumes/pelvis/data/prostate-MRI/rumc/images-reconverted/17687/17687_7809530920298551006434572382717573596_t2w.mha'
convert_to_prostate_quality_format(
    input_file='/Volumes/pelvis/data/prostate-MRI/umcg/images/M-222/M-222_223-0_hbv.mha',
    # Path to the missing file
    output_folder='/Volumes/pelvis/projects/tiago/DWI_IQA/data_dwi/raw/nnUnet_raw_data/Task001_ProstateQualityDWI/imagesTr',
    # Path to the output folder where images are stored
    sequence_number=574  # Sequence number for the missing file
)
