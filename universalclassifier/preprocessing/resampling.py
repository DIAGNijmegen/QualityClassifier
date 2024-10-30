import SimpleITK as sitk
import numpy as np

def resample_image(image, target_spacing=(.5, .5, 3.0), is_label=False):
    """
    Resamples a 3D image to the target spacing.

    Args:
        image (sitk.Image): The input image.
        target_spacing (tuple): Desired spacing in mm/voxel.
        is_label (bool): Whether the image is a label map.

    Returns:
        sitk.Image: The resampled image.
    """
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()

    # Calculate the new size based on target spacing
    new_size = [
        int(round(original_size[i] * (original_spacing[i] / target_spacing[i])))
        for i in range(3)
    ]

    resampler = sitk.ResampleImageFilter()
    resampler.SetOutputSpacing(target_spacing)
    resampler.SetSize(new_size)
    resampler.SetOutputDirection(image.GetDirection())
    resampler.SetOutputOrigin(image.GetOrigin())
    resampler.SetTransform(sitk.Transform())

    if is_label:
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resampler.SetInterpolator(sitk.sitkLinear)

    resampled_image = resampler.Execute(image)
    return resampled_image


def resample_and_normalize(data, target_spacing, properties, seg=None, force_separate_z=None):
    """
    Resamples the data and segmentation to the target spacing and normalizes the data.

    Args:
        data (numpy.ndarray): Image data of shape (c, x, y, z).
        target_spacing (list or tuple): Desired spacing [x, y, z].
        properties (dict): Metadata containing original spacing, direction, origin.
        seg (numpy.ndarray, optional): Segmentation data of shape (c, x, y, z).
        force_separate_z (bool, optional): Whether to handle the z-axis separately.

    Returns:
        tuple: (resampled_normalized_data, resampled_seg, updated_properties)
    """
    if force_separate_z:
        # Implement specific logic for separate z-axis handling
        # Placeholder: Modify target_spacing or resampling parameters based on force_separate_z
        print("Handling separate z-axis as per force_separate_z flag.")
        # Example: If force_separate_z is True, resample x and y, keep z unchanged
        new_spacing_xy = target_spacing[:2]
        new_spacing_z = properties["original_spacing"][2]  # Keep original z spacing

        # Resample x and y axes while keeping z spacing unchanged
        data_itk = sitk.GetImageFromArray(data)
        data_itk.SetSpacing(properties["original_spacing"])
        data_itk.SetDirection(properties["original_direction"])
        data_itk.SetOrigin(properties["original_origin"])

        resampler_xy = sitk.ResampleImageFilter()
        resampler_xy.SetOutputSpacing(new_spacing_xy + (properties["original_spacing"][2],))
        resampler_xy.SetSize([
            int(round(data_itk.GetSize()[i] * (data_itk.GetSpacing()[i] / new_spacing_xy[i])))
            for i in range(2)
        ] + [data_itk.GetSize()[2]])  # Keep z size unchanged
        resampler_xy.SetOutputDirection(data_itk.GetDirection())
        resampler_xy.SetOutputOrigin(data_itk.GetOrigin())
        resampler_xy.SetTransform(sitk.Transform())
        resampler_xy.SetInterpolator(sitk.sitkLinear)

        data_resampled_itk = resampler_xy.Execute(data_itk)
        data_resampled = sitk.GetArrayFromImage(data_resampled_itk)

        if seg is not None:
            seg_itk = sitk.GetImageFromArray(seg)
            seg_itk.SetSpacing(properties["original_spacing"])
            seg_itk.SetDirection(properties["original_direction"])
            seg_itk.SetOrigin(properties["original_origin"])

            resampler_xy.SetInterpolator(sitk.sitkNearestNeighbor)
            seg_resampled_itk = resampler_xy.Execute(seg_itk)
            seg_resampled = sitk.GetArrayFromImage(seg_resampled_itk)
        else:
            seg_resampled = None

        # Normalize data
        data_normalized = (data_resampled - np.mean(data_resampled)) / np.std(data_resampled)

        # Update properties
        properties["original_spacing"] = target_spacing[:2] + [properties["original_spacing"][2]]
        properties["resampled_size"] = data_resampled.shape[1:]  # excluding channel dimension

        return data_normalized, seg_resampled, properties
    else:
        # Default resampling logic
        data_itk = sitk.GetImageFromArray(data)
        seg_itk = sitk.GetImageFromArray(seg) if seg is not None else None

        # Set original spacing, direction, and origin
        data_itk.SetSpacing(properties["original_spacing"])
        data_itk.SetDirection(properties["original_direction"])
        data_itk.SetOrigin(properties["original_origin"])

        if seg_itk is not None:
            seg_itk.SetSpacing(properties["original_spacing"])
            seg_itk.SetDirection(properties["original_direction"])
            seg_itk.SetOrigin(properties["original_origin"])

        # Resample data
        data_resampled_itk = resample_image(data_itk, target_spacing=target_spacing, is_label=False)
        data_resampled = sitk.GetArrayFromImage(data_resampled_itk)

        # Resample segmentation
        if seg_itk is not None:
            seg_resampled_itk = resample_image(seg_itk, target_spacing=target_spacing, is_label=True)
            seg_resampled = sitk.GetArrayFromImage(seg_resampled_itk)
        else:
            seg_resampled = None

        # Normalize data (zero mean, unit variance)
        data_normalized = (data_resampled - np.mean(data_resampled)) / np.std(data_resampled)

        # Update properties
        properties["original_spacing"] = target_spacing
        properties["resampled_size"] = data_resampled.shape[1:]  # excluding channel dimension

        return data_normalized, seg_resampled, properties
