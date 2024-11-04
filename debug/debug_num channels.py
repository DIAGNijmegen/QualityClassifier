import numpy as np
import os
import matplotlib.pyplot as plt


preprocessed_folder = "/Volumes/pelvis/projects/tiago/DWI_IQA/data/preprocessed/Task001_ProstateQualityDWI/universal_classifier_plans_v1.0_stage0"  # Replace with actual path

for file in os.listdir(preprocessed_folder):
    if file.endswith('.npz'):
        data = np.load(os.path.join(preprocessed_folder, file))['data']
        print(f"{file}: {data.shape}")  # Check shape, especially the channels dimension

        # Check if it has at least 2 channels
        if data.shape[0] > 1:
            # Extract the second channel (index 1)
            second_channel = data[1]

            # Plot the second channel, adjusting for 3D nature if necessary
            plt.figure(figsize=(10, 8))
            plt.title(f"Second Channel - {file}")

            # Choose the middle slice along the z-axis (or modify as needed)
            z_middle = second_channel.shape[0] // 2
            plt.imshow(second_channel[z_middle], cmap='gray')
            plt.colorbar()
            plt.show()
        else:
            print(f"{file} has less than 2 channels.")