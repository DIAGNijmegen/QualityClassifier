# Getting Data Folder Structure

This folder contains scripts, data lists, and utilities for handling, filtering, and preparing MRI scans and datasets for further processing. Below is a breakdown of the folder structure and the purpose of each subdirectory.

## Folder Structure

- **1_get_procanceri_val_set**: Contains scripts and data for preparing validation sets specifically from the ProCancerI dataset. This folder likely includes configuration files and processing scripts tailored for ProCancerI data.


- **2_get_rumc_zgt_umcg_val_set**: Scripts and data for setting up validation sets from RUMC, ZGT, and UMCG sources. This folder handles data selection, filtering, and validation set preparation specific to these institutions.


- **3_get_promis_val_set**: Includes resources for generating validation sets from the PROMIS dataset. This may include scripts to filter and organize the data in the format required for processing and validation.


- **4_get_lq_dwi_lists**: Contains lists and scripts related to low-quality (LQ) Diffusion-Weighted Imaging (DWI) scans. This folder may include configuration files that identify low-quality images for exclusion or separate processing.


- **5_get_hq_dwi_lists**: Stores lists and scripts for high-quality (HQ) DWI scans. It likely includes identifiers or configuration files to process or select only high-quality scans.


- **6_copy_training_scans_to_folders**: Contains scripts to organize, filter, and copy training scans into appropriate folders. This folder likely includes scripts for dataset partitioning and transfer of training images into structured directories.


- **exclusion_lists**: Holds lists of scans or datasets that need to be excluded from processing. These lists may help in filtering out specific scans during data preparation steps.


- **utils**: Contains utility functions and helper scripts used across the various data processing and filtering tasks. Common utility scripts may include functions for loading configuration files, performing file conversions, logging, or data validation.

## Additional Files

- **check_failed_convertions.py**: This script checks for files that failed to convert, allowing you to identify issues in data processing and ensure no files are missing from the dataset.


- **convert_one_file.py**: A script to convert a single image file to the required format (e.g., `ProstateQualityDWI_0764_0000.nii.gz`). This can be used to manually handle specific files missing from the dataset or requiring special attention.


- **data_sorting_for_nnUnet.py**: Contains functions and logic to sort and organize data for nnU-Net, preparing images and labels in the required format and structure for nnU-Net processing.

## Useful Information

- **Data Preparation**: The `getting_data` folder provides all necessary tools for preparing datasets from multiple sources (e.g., ProCancerI, PROMIS, RUMC). Each subfolder focuses on specific dataset sources and quality filters.


- **High and Low Quality Lists**: `4_get_lq_dwi_lists` and `5_get_hq_dwi_lists` folders allow the separation of data by quality, which can be crucial for training models that are sensitive to image quality.


- **Utilities**: Utility scripts in `utils` simplify repetitive tasks like file loading, data validation, and conversion, ensuring consistency across all data preparation steps.


- **Conversion and Validation**: Use `check_failed_convertions.py` to verify successful conversions and `convert_one_file.py` to fix individual files. These scripts are essential for ensuring all images are correctly processed and organized.


- **Data Sorting for nnU-Net**: `data_sorting_for_nnUnet.py` is designed to help sort and organize data specifically for nnU-Net training. Make sure to follow nnU-Net's directory structure and naming conventions.

## Usage Tips

1. **Run Quality Filters First**: Use `4_get_lq_dwi_lists` and `5_get_hq_dwi_lists` to get high- and low-quality images listed if you used macos_tags to label them.
2. **Check Conversions**: After conversion, use `check_failed_convertions.py` to identify any missing files.
3. **Prepare for nnU-Net**: Ensure your data is correctly sorted using `data_sorting_for_nnUnet.py` and organized according to nnU-Net requirements before training.

This structure provides a robust setup for managing and preparing large MRI datasets for machine learning models, particularly those requiring careful quality assessment and dataset partitioning.
