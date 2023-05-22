from __future__ import print_function
import os
import cv2
import tqdm
import json
import argparse
import numpy as np
from PIL import Image
from imageio import imwrite
import torch
from torch.utils import data
from torch.utils.data import DataLoader
from torchvision import transforms
import Utils
from models.FCRN import MyModel as ResNet


def main():
    test_img = MyData(args.path)
    print('Test Data Num:', len(test_img))
    dataset_val = DataLoader(test_img, batch_size=1, num_workers=2, drop_last=False, pin_memory=True, shuffle=False)
    saver = Utils.ModelSaver('./save')
    from models.FCRN import MyModel as ResNet
    model = ResNet(layers=50, decoder='upproj', output_size=None, in_channels=3, pretrained=True).cuda()
    saver.LoadLatestModel(model, None)
    Run(dataset_val, model, (not args.nocrop))
