import os
import cv2
import numpy as np
import random
import torch
from torch.nn import functional as F
from torch.utils import data


def __getitem__(self, index):
    item = self.files[index]
    name = item['name']
    image = cv2.imread(os.path.join(self.root, 'LookIntoPerson/TrainVal_images/', item['img']), cv2.IMREAD_COLOR)
    label = cv2.imread(os.path.join(self.root, 'LookIntoPerson/TrainVal_parsing_annotations/', item['label']), cv2.IMREAD_GRAYSCALE)
    size = label.shape
    if ('testval' in self.list_path):
        image = cv2.resize(image, self.crop_size, interpolation=cv2.INTER_LINEAR)
        image = self.input_transform(image)
        image = image.transpose((2, 0, 1))
        return (image.copy(), label.copy(), np.array(size), name)
    if self.flip:
        flip = ((np.random.choice(2) * 2) - 1)
        image = image[(:, ::flip, :)]
        label = label[(:, ::flip)]
        if (flip == (- 1)):
            right_idx = [15, 17, 19]
            left_idx = [14, 16, 18]
            for i in range(0, 3):
                right_pos = np.where((label == right_idx[i]))
                left_pos = np.where((label == left_idx[i]))
                label[(right_pos[0], right_pos[1])] = left_idx[i]
                label[(left_pos[0], left_pos[1])] = right_idx[i]
    (image, label) = self.resize_image(image, label, self.crop_size)
    (image, label) = self.gen_sample(image, label, self.multi_scale, False)
    return (image.copy(), label.copy(), np.array(size), name)
