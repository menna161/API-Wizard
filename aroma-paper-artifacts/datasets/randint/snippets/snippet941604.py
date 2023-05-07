import os.path
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
import random
import torchvision.transforms as transforms
import numpy as np


def __getitem__(self, index):
    'Return a data point and its metadata information.\n\n        Parameters:\n            index -- a random integer for data indexing\n\n        Returns:\n            a dictionary of data with their names. It usually contains the data itself and its metadata information.\n\n        '
    is_natural = (random.random() <= 0.3)
    if (self.opt.phase == 'train'):
        if is_natural:
            natural_index = (index % self.natural_size)
            A1_path = self.natural_A1_paths[natural_index]
            B_path = self.natural_B_paths[natural_index]
            A1_img = np.asarray(Image.open(A1_path).convert('RGB'))
            A2_img = Image.fromarray(np.zeros_like(A1_img))
            B_img = np.asarray(Image.open(B_path).convert('RGB'))
            imgs = self.crop({'I': B_img, 'T': A1_img})
            (A1_img, B_img) = (Image.fromarray(imgs['T']), Image.fromarray(imgs['I']))
            is_natural_int = 1
        else:
            A1_path = self.A1_paths[(index % self.A1_size)]
            index_A2 = random.randint(0, (self.A2_size - 1))
            A2_path = self.A2_paths[index_A2]
            B_path = ''
            A1_img = Image.open(A1_path).convert('RGB')
            A2_img = Image.open(A2_path).convert('RGB')
            B_img = Image.fromarray(np.zeros_like(A1_img))
            is_natural_int = 0
    else:
        B_path = self.B_paths[index]
        B_img = Image.open(B_path).convert('RGB')
        if (index < len(self.A1_paths)):
            A1_path = self.A1_paths[index]
            A1_img = Image.open(A1_path).convert('RGB')
        else:
            A1_img = Image.fromarray(np.zeros_like(B_img))
        A2_img = None
        is_natural_int = 1
    (w, h) = A1_img.size
    neww = ((w // 4) * 4)
    newh = ((h // 4) * 4)
    resize = transforms.Resize([newh, neww])
    A1_img = resize(A1_img)
    A2_img = (resize(A2_img) if A2_img else None)
    B_img = resize(B_img)
    A1 = self.transform_A(A1_img)
    A2 = (self.transform_A(A2_img) if A2_img else None)
    B = self.transform_B(B_img)
    T2 = self.trans2(A1_img)
    T4 = self.trans4(A1_img)
    if (A2 is not None):
        return {'T': A1, 'T2': T2, 'T4': T4, 'R': A2, 'I': B, 'B_paths': B_path, 'isNatural': is_natural_int}
    else:
        return {'T': A1, 'T2': T2, 'T4': T4, 'I': B, 'B_paths': B_path, 'isNatural': is_natural_int}
