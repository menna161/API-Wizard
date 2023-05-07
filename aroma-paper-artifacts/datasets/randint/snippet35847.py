from typing import List, Tuple
import tensorflow as tf
import random


def __init__(self, image_paths: List[str], mask_paths: List[str], image_size: Tuple[int], channels: Tuple[int]=(3, 3), crop_percent: float=None, seed: int=None, augment: bool=True, compose: bool=False, one_hot_encoding: bool=False, palette=None):
    '\n        Initializes the data loader object\n        Args:\n            image_paths: List of paths of train images.\n            mask_paths: List of paths of train masks (segmentation masks)\n            image_size: Tuple, the final height, width of the loaded images.\n            channels: Tuple of ints, first element is number of channels in images,\n                      second is the number of channels in the mask image (needed to\n                      correctly read the images into tensorflow and apply augmentations)\n            crop_percent: Float in the range 0-1, defining percentage of image \n                          to randomly crop.\n            palette: A list of RGB pixel values in the mask. If specified, the mask\n                     will be one hot encoded along the channel dimension.\n            seed: An int, if not specified, chosen randomly. Used as the seed for \n                  the RNG in the data pipeline.\n        '
    self.image_paths = image_paths
    self.mask_paths = mask_paths
    self.palette = palette
    self.image_size = image_size
    self.augment = augment
    self.compose = compose
    self.one_hot_encoding = one_hot_encoding
    if (crop_percent is not None):
        if (0.0 < crop_percent <= 1.0):
            self.crop_percent = tf.constant(crop_percent, tf.float32)
        elif (0 < crop_percent <= 100):
            self.crop_percent = tf.constant((crop_percent / 100.0), tf.float32)
        else:
            raise ValueError('Invalid value entered for crop size. Please use an                                   integer between 0 and 100, or a float between 0 and 1.0')
    else:
        self.crop_percent = None
    self.channels = channels
    if (seed is None):
        self.seed = random.randint(0, 1000)
    else:
        self.seed = seed
