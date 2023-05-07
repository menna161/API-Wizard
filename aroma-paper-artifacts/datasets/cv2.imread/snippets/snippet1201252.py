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


def __getitem__(self, idx):
    imageid = self.image_ids[idx]
    im = get_image(imageid, basepath=self.basepath, rgbdir='train_rgb')
    assert (im is not None)
    locid = '_'.join(imageid.split('_')[(- 2):])
    mask = cv2.imread(f'{self.basepath}/masks/mask_{locid}.tif', cv2.IMREAD_GRAYSCALE)
    assert (mask is not None)
    augmented = self.aug(image=im, mask=mask)
    mask_ = (augmented['mask'] > 0).astype(np.uint8)
    mask_ = torch.from_numpy(np.expand_dims(mask_, 0)).float()
    label_ = torch.from_numpy(np.expand_dims(augmented['mask'], 0)).float()
    return (img_to_tensor(augmented['image']), mask_, label_, imageid)
