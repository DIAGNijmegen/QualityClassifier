import numpy as np

def central_pad_data_or_seg(np_image, target_size, outside_val=0):
    """
    Centrally pads a 4D numpy array (channels, x, y, z) to the target size.

    Args:
        np_image (numpy.ndarray): Image or segmentation data of shape (c, x, y, z).
        target_size (list or tuple): Desired size [x, y, z].
        outside_val (int or float, optional): Value to pad with. Defaults to 0.

    Returns:
        numpy.ndarray: Padded image or segmentation data of shape (c, target_x, target_y, target_z).
    """
    target_size = np.asarray([np_image.shape[0]] + list(target_size), dtype=int)

    assert len(np_image.shape) == 4, "Input must be a 4D array (c, x, y, z)."
    assert all([s1 <= s2 for s1, s2 in zip(np_image.shape, target_size)]), "Only padding is supported, no cropping."

    output_image = np.full(target_size, outside_val, np_image.dtype)

    offsets = []
    for i, sh in enumerate(target_size):
        if i == 0:
            # Keep all channels
            offsets.append(slice(None))
        else:
            # Compute offset to center the image
            start = (sh // 2) - (np_image.shape[i] // 2)
            offset = slice(start, start + np_image.shape[i])
            offsets.append(offset)

    output_image[tuple(offsets)] = np_image
    return output_image


def central_pad(data, target_size, properties, seg):
    """
    Applies central padding to both data and segmentation arrays.

    Args:
        data (numpy.ndarray): Image data of shape (c, x, y, z).
        target_size (list or tuple): Desired size [x, y, z].
        properties (dict): Metadata dictionary to update with padding information.
        seg (numpy.ndarray): Segmentation data of shape (c, x, y, z).

    Returns:
        tuple: Padded data, padded segmentation, and updated properties.
    """
    assert not ((data is None) and (seg is None)), "Both data and seg cannot be None."
    if data is not None:
        assert len(data.shape) == 4, "Data must be a 4D array (c, x, y, z)."
    if seg is not None:
        assert len(seg.shape) == 4, "Segmentation must be a 4D array (c, x, y, z)."

    if data is not None:
        shape = np.array(data[0].shape)
    else:
        shape = np.array(seg[0].shape)

    print(f"Applying uniform padding from {shape} to {target_size}...")
    if data is not None:
        data = central_pad_data_or_seg(data, target_size, outside_val=0)
    if seg is not None:
        seg = central_pad_data_or_seg(seg, target_size, outside_val=0)

    properties['size_after_central_pad'] = target_size
    return data, seg, properties
