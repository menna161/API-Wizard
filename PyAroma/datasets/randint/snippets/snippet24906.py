import torch.utils.data as data
import numpy as np
import os
from torchvision import transforms
from PIL import Image


def __getitem__(self, index):
    file_path = self.file_list[index][0]
    sample = Image.open(file_path)
    while (sample.layers != 3):
        index = np.random.randint(256, 120000)
        file_path = self.file_list[index][0]
        sample = Image.open(file_path)
    if self.transform:
        sample = self.transform(sample)
    return (sample, int(self.file_list[index][1]))
