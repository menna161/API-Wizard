import os, glob
import torch
import numpy as np
import scipy.io
from skimage.color import rgb2lab
import matplotlib.pyplot as plt


def __getitem__(self, idx):
    idx = self.index[idx][:(- 4)]
    gt = scipy.io.loadmat(os.path.join(self.gt_dir, (idx + '.mat')))
    t = np.random.randint(0, len(gt['groundTruth'][0]))
    gt = gt['groundTruth'][0][t][0][0][0]
    img = rgb2lab(plt.imread(os.path.join(self.img_dir, (idx + '.jpg'))))
    gt = gt.astype(np.int64)
    img = img.astype(np.float32)
    if (self.color_transforms is not None):
        img = self.color_transforms(img)
    if (self.geo_transforms is not None):
        (img, gt) = self.geo_transforms([img, gt])
    gt = convert_label(gt)
    gt = torch.from_numpy(gt)
    img = torch.from_numpy(img)
    img = img.permute(2, 0, 1)
    return (img, gt.reshape(50, (- 1)).float())
