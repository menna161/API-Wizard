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


def get_image(imageid, basepath='/wdata/dataset', rgbdir='train_rgb'):
    fn = f'{basepath}/{rgbdir}/Pan-Sharpen_{imageid}.tif'
    img = cv2.imread(fn, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
