from __future__ import print_function
import os
import sys
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import Utils
from . import Equirec2Cube as E2C

if (__name__ == '__main__'):
    img = cv2.imread('src/image.jpg', cv2.IMREAD_COLOR)
    img = resize(img, 0.22)
    [h, w, _] = img.shape
    equirec = EquirecRotate(h, w)
    BS = 3
    e2c = E2C.Equirec2Cube(BS, h, w, 256, 90)
    print(e2c.intrisic)
    print(img.shape)
    batch = img.reshape([1, h, w, 3])
    batch = np.swapaxes(batch, 1, 3)
    batch = np.swapaxes(batch, 2, 3)
    tmp = [batch for x in range(BS)]
    batch = np.concatenate(tmp, axis=0)
    angle = np.zeros([BS, 2])
    angle[(0, 0)] = ((180.0 / 180) * np.pi)
    angle[(0, 1)] = ((90.0 / 180) * np.pi)
    angle[(1, 0)] = ((20.0 / 180) * np.pi)
    angle[(1, 1)] = ((30.0 / 180) * np.pi)
    angle[(2, 0)] = (((- 60.0) / 180) * np.pi)
    angle[(2, 1)] = ((23.0 / 180) * np.pi)
    batch = torch.FloatTensor((batch.astype(np.float32) / 255)).cuda()
    angle = torch.FloatTensor(angle).cuda()
    result = equirec.Rotate(batch, angle)
    cubes = e2c.ToCubeTensor(result)
    cv2.namedWindow('GG')
    for i in range(BS):
        origin = batch[(i, :, :, :)].transpose(0, 2).transpose(0, 1).cpu().numpy()
        new = result[(i, :, :, :)].transpose(0, 2).transpose(0, 1).data.cpu().numpy()
        big = resize(np.concatenate([origin, new], axis=0), 0.5)
        cv2.imshow('GG', big)
        cv2.waitKey(0)
        for j in range(6):
            cube = cubes[(((i * 6) + j), :, :, :)].transpose(0, 2).transpose(0, 1).data.cpu().numpy()
            cv2.imshow('GG', cube)
            cv2.waitKey(0)
