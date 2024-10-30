import numpy as np
import pickle
import os
from nnunet.configuration import default_num_threads
from nnunet.preprocessing.cropping import get_case_identifier_from_npz
from batchgenerators.utilities.file_and_folder_operations import *
from multiprocessing.pool import Pool
from nnunet.preprocessing.preprocessing import GenericPreprocessor
from universalclassifier.preprocessing.cropping import ClassificationImageCropper
from universalclassifier.preprocessing.resampling import resample_and_normalize
from universalclassifier.preprocessing.padding import central_pad  # Import padding function

class UniversalClassifierPreprocessor(GenericPreprocessor):

    def run(self, target_spacings, target_sizes, input_folder_with_cropped_npz, output_folder, data_identifier,
            num_threads=default_num_threads, force_separate_z=None):
        """
        Runs the preprocessing pipeline.

        Args:
            target_spacings (list of lists): Desired voxel spacings for each stage, e.g., [[1.0, 1.0, 1.0]].
            target_sizes (list of lists): Desired output sizes for each stage, e.g., [[128, 128, 128]].
            input_folder_with_cropped_npz (str): Path to the folder containing cropped NPZ files.
            output_folder (str): Path to the folder where preprocessed data will be saved.
            data_identifier (str): Identifier for the dataset.
            num_threads (int or list of ints, optional): Number of threads for multiprocessing. Defaults to default_num_threads.
            force_separate_z (bool, optional): Parameter for handling separate z-axis if needed. Defaults to None.
        """
        print("Initializing to run preprocessing")
        print("npz folder:", input_folder_with_cropped_npz)
        print("output_folder:", output_folder)
        list_of_cropped_npz_files = subfiles(input_folder_with_cropped_npz, True, None, ".npz", True)
        maybe_mkdir_p(output_folder)
        num_stages = len(target_spacings)
        if not isinstance(num_threads, (list, tuple, np.ndarray)):
            num_threads = [num_threads] * num_stages

        assert len(num_threads) == num_stages, "Number of threads must match number of stages."

        for i in range(num_stages):
            all_args = []
            output_folder_stage = os.path.join(output_folder, f"{data_identifier}_stage{i}")
            maybe_mkdir_p(output_folder_stage)
            spacing = target_spacings[i]
            target_size = target_sizes[i]
            for j, case in enumerate(list_of_cropped_npz_files):
                case_identifier = get_case_identifier_from_npz(case)
                args = (spacing, target_size, case_identifier, output_folder_stage, input_folder_with_cropped_npz, force_separate_z)
                all_args.append(args)
            with Pool(num_threads[i]) as p:
                p.starmap(self._run_internal, all_args)

    def _run_internal(self, target_spacing, target_size, case_identifier, output_folder_stage, cropped_output_dir,
                      force_separate_z):
        """
        Internal method to handle preprocessing of a single case.

        Args:
            target_spacing (list or tuple): Desired voxel spacing [x, y, z].
            target_size (list or tuple): Desired output size [x, y, z].
            case_identifier (str): Identifier for the case.
            output_folder_stage (str): Path to the output folder for the current stage.
            cropped_output_dir (str): Path to the cropped data directory.
            force_separate_z (bool, optional): Parameter for handling separate z-axis if needed.
        """
        data, seg, properties = self.load_cropped(cropped_output_dir, case_identifier)

        data = data.transpose((0, *[i + 1 for i in self.transpose_forward]))
        seg = seg.transpose((0, *[i + 1 for i in self.transpose_forward]))

        # Resample and normalize using the resampling module
        data, seg, properties = resample_and_normalize(
            data, target_spacing, properties, seg, force_separate_z
        )

        # Apply central padding using the padding module
        data, seg, properties = central_pad(data, target_size, properties, seg)

        # Combine data and segmentation for saving
        all_data = np.vstack((data, seg)).astype(np.float32)
        print(f"Saving: {os.path.join(output_folder_stage, f'{case_identifier}.npz')}")
        np.savez_compressed(
            os.path.join(output_folder_stage, f"{case_identifier}.npz"),
            data=all_data
        )
        with open(os.path.join(output_folder_stage, f"{case_identifier}.pkl"), 'wb') as f:
            pickle.dump(properties, f)

    def preprocess_test_case(self, data_files, target_spacing, target_size, seg_file=None, force_separate_z=None):
        """
        Preprocesses a single test case.

        Args:
            data_files (list): List of paths to image files.
            target_spacing (list or tuple): Desired voxel spacing [x, y, z].
            target_size (list or tuple): Desired output size [x, y, z].
            seg_file (str, optional): Path to the segmentation file. Defaults to None.
            force_separate_z (bool, optional): Parameter for handling separate z-axis if needed. Defaults to None.

        Returns:
            tuple: Preprocessed data, segmentation, and updated properties.
        """
        data, seg, properties = ClassificationImageCropper.crop_from_list_of_files(
            data_files, seg_file, create_dummy_seg=(seg_file is None)
        )

        data = data.transpose((0, *[i + 1 for i in self.transpose_forward]))
        seg = seg.transpose((0, *[i + 1 for i in self.transpose_forward]))

        # Resample and normalize using the resampling module
        data, seg, properties = resample_and_normalize(
            data, target_spacing, properties, seg, force_separate_z
        )

        # Apply central padding using the padding module
        data, seg, properties = central_pad(data, target_size, properties, seg)

        return data.astype(np.float32), seg, properties
