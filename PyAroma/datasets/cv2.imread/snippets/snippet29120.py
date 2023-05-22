import os
import json
from PIL import Image
import cv2
import numpy as np
import random
import torch
from torch.nn import functional as F
from torch.utils import data


def __getitem__(self, index):
    item = self.files[index]
    name = item['name']
    image = cv2.imread(os.path.join(self.root, item['img']), cv2.IMREAD_COLOR)
    size = image.shape
    label = cv2.imread(os.path.join(self.root, item['label']), cv2.IMREAD_GRAYSCALE)
    label = self.convert_label(label)
    if ('validation' in self.list_path):
        image = self.input_transform(image)
        image = image.transpose((2, 0, 1))
        label = self.label_transform(label)
    else:
        (image, label) = self.resize_image_label(image, label, self.base_size)
        (image, label) = self.gen_sample(image, label, self.multi_scale, self.flip, self.center_crop_test)
    return (image.copy(), label.copy(), np.array(size), name)
