from __future__ import print_function
import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import time

if (__name__ == '__main__'):
    img = cv2.imread('/media/external/Fu-En.Wang/Data/360/final/rotated/117a5a3b1cd3298e31aeaae786c6bf02/0.txt/14_color.png', cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    origin = (img.astype(float).copy() / 255)
    img = img.reshape([1, 512, 1024, 3]).swapaxes(1, 3).swapaxes(2, 3)
    img = (img.astype(float) / 255)
    batch = torch.FloatTensor(img).cuda()
    ER = EquirecRotate(512, 1024)
    angle = torch.FloatTensor(np.array([0, 90, 0]).reshape([1, 3])).cuda()
    angle = ((angle / 180) * np.pi)
    import time
    a = time.time()
    c = 1
    for i in range(c):
        print(i)
        batch = ER.Rotate(batch, angle)
        after = batch.view(3, 512, 1024).transpose(0, 2).transpose(0, 1).data.cpu().numpy()
    b = time.time()
    print(('FPS: %lf' % (c / (b - a))))
    big = np.concatenate([origin, after], axis=0)
    plt.imshow(big)
    plt.show()
