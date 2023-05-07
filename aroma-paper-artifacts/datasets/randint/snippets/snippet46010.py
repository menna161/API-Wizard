import os
import random
import numpy as np
import torch
import torch.utils.data
from data import hd3data
from datasets import data_utils


def __call__(self, image, flow, prob, label):
    if (self.crop_shape is not None):
        label_shape = label.shape[:2]
        if (label_shape < self.crop_shape):
            raise Exception('Label too small for given crop_shape.')
        start_height = random.randint(0, (label_shape[0] - self.crop_shape[0]))
        end_height = (start_height + self.crop_shape[0])
        start_width = random.randint(0, (label_shape[1] - self.crop_shape[1]))
        end_width = (start_width + self.crop_shape[1])
        label = label[(start_height:end_height, start_width:end_width, :)]
        image = image[(start_height:end_height, start_width:end_width, :)]
        flow = flow[(start_height:end_height, start_width:end_width, :)]
        prob = prob[(start_height:end_height, start_width:end_width, :)]
    for (i, (channel_mean, channel_std)) in enumerate(zip(self.mean, self.std)):
        image[(:, :, i)] = ((image[(:, :, i)] - channel_mean) / channel_std)
    return (image, flow, prob, label)
