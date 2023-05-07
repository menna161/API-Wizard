import torch
import random
import cv2
import collections
import numpy as np
from skimage.filters import gaussian
from scipy.ndimage import zoom as scizoom
import torchvision.transforms as transforms


def blur_data(batch, patch_size, device):
    batch = batch.cpu()
    convert_img = transforms.Compose([transforms.ToPILImage()])
    convert_tensor = transforms.Compose([transforms.ToTensor()])
    blurs = get_blurs()
    random_method = random.choice(list(blurs.keys()))
    for i in range(len(batch)):
        severity = random.randint(0, 5)
        if (severity > 0):
            blur = (lambda clean_img: blurs[random_method](clean_img, severity, patch_size))
            batch[i] = (convert_tensor(blur(convert_img(batch[i]))).float() / 255.0)
    return batch.to(device)
