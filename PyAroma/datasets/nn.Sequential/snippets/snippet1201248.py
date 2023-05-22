import warnings
from pathlib import Path
import tempfile
import csv
import os
import datetime
import json
import shutil
import time
import sys
import scipy.sparse as ss
import numpy as np
import pandas as pd
import attr
import click
import tqdm
import cv2
import rasterio
import skimage.measure
from sklearn.utils import Bunch
from torch import nn
import torch
from torch.optim import Adam
from torchvision.models import vgg16
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.sampler import SequentialSampler, RandomSampler
from albumentations.torch.functional import img_to_tensor
from albumentations import Normalize, Compose, HorizontalFlip, RandomRotate90, RandomCrop, CenterCrop
import spacenetutilities.labeltools.coreLabelTools as cLT
from spacenetutilities import geoTools as gT
from shapely.geometry import shape
from shapely.wkt import dumps
import geopandas as gpd


def __init__(self, num_filters=32, pretrained=False):
    super().__init__()
    self.encoder = vgg16(pretrained=pretrained).features
    self.pool = nn.MaxPool2d(2, 2)
    self.relu = nn.ReLU(inplace=True)
    self.conv1 = nn.Sequential(self.encoder[0], self.relu, self.encoder[2], self.relu)
    self.conv2 = nn.Sequential(self.encoder[5], self.relu, self.encoder[7], self.relu)
    self.conv3 = nn.Sequential(self.encoder[10], self.relu, self.encoder[12], self.relu, self.encoder[14], self.relu)
    self.conv4 = nn.Sequential(self.encoder[17], self.relu, self.encoder[19], self.relu, self.encoder[21], self.relu)
    self.conv5 = nn.Sequential(self.encoder[24], self.relu, self.encoder[26], self.relu, self.encoder[28], self.relu)
    self.center = decoder_block(512, ((num_filters * 8) * 2), (num_filters * 8))
    self.dec5 = decoder_block((512 + (num_filters * 8)), ((num_filters * 8) * 2), (num_filters * 8))
    self.dec4 = decoder_block((512 + (num_filters * 8)), ((num_filters * 8) * 2), (num_filters * 8))
    self.dec3 = decoder_block((256 + (num_filters * 8)), ((num_filters * 4) * 2), (num_filters * 2))
    self.dec2 = decoder_block((128 + (num_filters * 2)), ((num_filters * 2) * 2), num_filters)
    self.dec1 = conv_relu((64 + num_filters), num_filters)
    self.final = nn.Conv2d(num_filters, 1, kernel_size=1)
