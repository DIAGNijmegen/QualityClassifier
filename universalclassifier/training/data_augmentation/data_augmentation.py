from universalclassifier.training.data_augmentation.transforms import RescaleSegmentationTransform
from batchgenerators.dataloading.multi_threaded_augmenter import MultiThreadedAugmenter
from batchgenerators.transforms.abstract_transforms import Compose
from batchgenerators.transforms.color_transforms import GammaTransform, ContrastAugmentationTransform
from batchgenerators.transforms.noise_transforms import GaussianNoiseTransform
from batchgenerators.transforms.spatial_transforms import SpatialTransform, MirrorTransform
from batchgenerators.transforms.utility_transforms import RemoveLabelTransform, NumpyToTensor
from universalclassifier.training.data_augmentation.transforms import RescaleSegmentationTransform


def get_moreDA_augmentation(dataloader_train, dataloader_val, patch_size, params, pin_memory=True):
    tr_transforms = [
        # Spatial Transform with rotation and scaling
        SpatialTransform(
            patch_size,
            do_rotation=True,
            angle_x=params.get("rotation_x"),
            angle_y=params.get("rotation_y"),
            angle_z=params.get("rotation_z"),
            p_rot_per_axis=params.get("rotation_p_per_axis"),
            do_scale=True,
            scale=params.get("scale_range"),
            border_mode_data="constant",
            border_cval_data=0,
            border_mode_seg="constant",
            order_seg=1,
            random_crop=True
        ),
        MirrorTransform(params.get("mirror_axes")),

        # Intensity adjustments (MRI-specific)
        GammaTransform(params.get("gamma_range"), invert_image=True, retain_stats=True, p_per_sample=0.1),
        ContrastAugmentationTransform(p_per_sample=0.15),

        # Additional transforms
        RescaleSegmentationTransform(params.get("num_seg_classes")),
        RemoveLabelTransform(-1, 0),
        NumpyToTensor(['data'], 'float'),
        NumpyToTensor(['target'], 'long')
    ]
    tr_transforms = Compose(tr_transforms)

    # Train and validation augmentation
    batchgenerator_train = MultiThreadedAugmenter(dataloader_train, tr_transforms, params.get('num_threads'),
                                                  params.get("num_cached_per_thread"), pin_memory=pin_memory)
    batchgenerator_val = MultiThreadedAugmenter(dataloader_val, tr_transforms, max(params.get('num_threads') // 2, 1),
                                                params.get("num_cached_per_thread"), pin_memory=pin_memory)

    return batchgenerator_train, batchgenerator_val

