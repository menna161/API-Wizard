import os
import os.path
import cv2
import numpy as np
from PIL import Image
import time
from torch.utils.data import Dataset
import torch


def __getitem__(self, index):
    (image_path, label_path) = self.data_list[index]
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.float32(image)
    label = np.array(Image.open(label_path))
    if ((image.shape[0] != label.shape[0]) or (image.shape[1] != label.shape[1])):
        raise RuntimeError((((('Image & label shape mismatch: ' + image_path) + ' ') + label_path) + '\n'))
    if (self.transform is not None):
        (image, label) = self.transform(image, label)
    return (image, label)
