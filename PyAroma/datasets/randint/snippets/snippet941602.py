import os.path
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
import random
import torchvision.transforms as transforms
import numpy as np


def __call__(self, sample):
    (image, landmarks) = (sample['I'], sample['T'])
    (h, w) = image.shape[:2]
    min_a = min(h, w)
    self.output_size = (((min_a * 7) // 10), ((min_a * 7) // 10))
    (new_h, new_w) = self.output_size
    top = np.random.randint(0, (h - new_h))
    left = np.random.randint(0, (w - new_w))
    image = image[(top:(top + new_h), left:(left + new_w))]
    landmarks = landmarks[(top:(top + new_h), left:(left + new_w))]
    return {'I': image, 'T': landmarks}
