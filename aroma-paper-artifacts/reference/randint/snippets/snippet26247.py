import random
from typing import Any
from torch import Tensor
from numpy import ndarray
import cv2
import numpy as np
import torch
from torchvision.transforms import functional as F_vision


def random_crop(images: (((ndarray | Tensor) | list[ndarray]) | list[Tensor]), patch_size: int) -> ([ndarray] or [Tensor] or [list[ndarray]] or [list[Tensor]]):
    if (not isinstance(images, list)):
        images = [images]
    input_type = ('Tensor' if torch.is_tensor(images[0]) else 'Numpy')
    if (input_type == 'Tensor'):
        (image_height, image_width) = images[0].size()[(- 2):]
    else:
        (image_height, image_width) = images[0].shape[0:2]
    top = random.randint(0, (image_height - patch_size))
    left = random.randint(0, (image_width - patch_size))
    if (input_type == 'Tensor'):
        images = [image[:, :, top:(top + patch_size), left:(left + patch_size)] for image in images]
    else:
        images = [image[top:(top + patch_size), left:(left + patch_size), ...] for image in images]
    if (len(images) == 1):
        images = images[0]
    return images
