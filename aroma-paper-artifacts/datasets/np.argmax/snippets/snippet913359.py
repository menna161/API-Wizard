import os
import logging
import argparse
import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.nn.functional as F
import torch.nn.parallel
import torch.utils.data
from util import config
from util.util import colorize
from model.pspnet import PSPNet
from model.psanet import PSANet


def test(model, image_path, classes, mean, std, base_size, crop_h, crop_w, scales, colors):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    (h, w, _) = image.shape
    prediction = np.zeros((h, w, classes), dtype=float)
    for scale in scales:
        long_size = round((scale * base_size))
        new_h = long_size
        new_w = long_size
        if (h > w):
            new_w = round(((long_size / float(h)) * w))
        else:
            new_h = round(((long_size / float(w)) * h))
        image_scale = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        prediction += scale_process(model, image_scale, classes, crop_h, crop_w, h, w, mean, std)
    prediction = scale_process(model, image_scale, classes, crop_h, crop_w, h, w, mean, std)
    prediction = np.argmax(prediction, axis=2)
    gray = np.uint8(prediction)
    color = colorize(gray, colors)
    image_name = image_path.split('/')[(- 1)].split('.')[0]
    gray_path = os.path.join('./figure/demo/', (image_name + '_gray.png'))
    color_path = os.path.join('./figure/demo/', (image_name + '_color.png'))
    cv2.imwrite(gray_path, gray)
    color.save(color_path)
    logger.info('=> Prediction saved in {}'.format(color_path))
