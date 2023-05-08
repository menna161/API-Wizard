import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
import numpy as np
from tqdm import tqdm
import cv2
from PIL import Image
from models.fastscnn import FastSCNN
import os


def testImg(filename):
    seg = FSCNNSegModel(MDL_CLS, WEIGHTS_PATH)
    img = []
    im = cv2.imread(filename)
    img.append(im)
    bimgs = seg.imgProcess(img)
    result = seg.detect(bimgs)
    target = np.uint8(result[0])
    color = seg.colorArray()
    gray = seg.colorize(target, color)
    gray.save('target.png')
    pass
