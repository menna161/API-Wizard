import argparse
import os
import random
import shutil
import sys
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
from chainer import reporter
from chainer import training
from chainer.functions.evaluation import accuracy
from chainer.training import extensions
import onnx_chainer
import alex
import nin
import resnet50


def get_example(self, i):
    crop_size = self.crop_size
    (image, label) = self.base[i]
    (_, h, w) = image.shape
    if self.random:
        top = random.randint(0, ((h - crop_size) - 1))
        left = random.randint(0, ((w - crop_size) - 1))
        if random.randint(0, 1):
            image = image[(:, :, ::(- 1))]
    else:
        top = ((h - crop_size) // 2)
        left = ((w - crop_size) // 2)
    bottom = (top + crop_size)
    right = (left + crop_size)
    image = image[(:, top:bottom, left:right)]
    image -= self.mean[(:, top:bottom, left:right)]
    image *= (1.0 / 255.0)
    return (image, label)
