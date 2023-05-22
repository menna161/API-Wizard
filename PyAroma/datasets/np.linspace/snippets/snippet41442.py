import os, numpy as np, cv2, torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms
from skimage.io import imread
from skimage.transform import resize
import sys


def extract_camera_motion(self, img):
    m = min(img.shape[:2])
    if (m < 172):
        scale = int((172.0 / m))
        img = resize(img, ((scale * img.shape[0]), (scale * img.shape[1])), mode='constant', anti_aliasing=True)
        img = (255 * img).astype('uint8')
    elif (m > 512):
        scale = (512.0 / m)
        new_shape = (int((scale * img.shape[0])), int((scale * img.shape[1])))
        img = resize(img, new_shape, mode='constant', anti_aliasing=True)
        img = (255 * img).astype('uint8')
    if ((len(img.shape) == 2) or (img.shape[2] == 1)):
        img = np.repeat(img.reshape([img.shape[0], img.shape[1], 1]), 3, 2)
    if (img.shape[2] == 2):
        img = np.concatenate([img[(:, :, 0)], img[(:, :, 1)], img[(:, :, 1)]], 2)
    if (img.shape[2] == 4):
        img = img[(:, :, :3)]
    s = img.shape
    crop = self.crop_size
    N = (self.n_clips * self.clip_len)
    start = [np.random.randint(0, max((s[i] - crop), 1)) for i in range(2)]
    start_side = np.random.randint(crop, max(min((s[0] - start[0]), (s[1] - start[1])), (crop + 1)))
    end = [np.random.randint(0, max((s[i] - crop), 1)) for i in range(2)]
    end_side = np.random.randint(crop, max(min((s[0] - end[0]), (s[1] - end[1])), (crop + 1)))
    trajectory = [np.linspace(start[0], end[0], N).astype(int), np.linspace(start[1], end[1], N).astype(int), np.linspace(start_side, end_side, N).astype(int)]
    trajectory = np.stack(trajectory).T
    clip = []
    for tj in trajectory:
        im = img[(tj[0]:(tj[0] + tj[2]), tj[1]:(tj[1] + tj[2]))]
        assert ((len(img.shape) == 3) and (img.shape[2] == 3)), str(img.shape)
        im = self.crop_transform(im)
        clip.append(im)
    clip = torch.stack(clip)
    clip = clip.reshape(self.n_clips, self.clip_len, 3, self.crop_size, self.crop_size).transpose(1, 2)
    return clip
