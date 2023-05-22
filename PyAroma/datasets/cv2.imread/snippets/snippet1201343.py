import os
from os import path, makedirs, listdir
import sys
import numpy as np
import random
import torch
from torch import nn
from torch.backends import cudnn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.optim.lr_scheduler as lr_scheduler
from adamw import AdamW
from losses import dice_round, ComboLoss
import pandas as pd
from tqdm import tqdm
import timeit
import cv2
from zoo.models import ScSeSenet154_9ch_Unet
from imgaug import augmenters as iaa
from utils import preprocess_inputs, parse_img_id, dice


def __getitem__(self, idx):
    fn = (self.image_ids[idx] + '.png')
    img = cv2.imread(path.join(train_dir, fn), cv2.IMREAD_COLOR)
    img2 = cv2.imread(path.join(train_dir2, fn), cv2.IMREAD_COLOR)
    img3 = cv2.imread(path.join(train_dir3, fn), cv2.IMREAD_COLOR)
    msk = cv2.imread(path.join(masks_folder, fn), cv2.IMREAD_COLOR)
    msk = ((msk > 127) * 1)
    msk = msk[(..., :2)]
    img = np.concatenate([img, img2, img3], axis=2)
    img = img[(98:(- 98), 98:(- 98), ...)]
    msk = msk[(98:(- 98), 98:(- 98), ...)]
    img = preprocess_inputs(img)
    (nadir, cat_inp, coord_inp) = parse_img_id(fn)
    img = torch.from_numpy(img.transpose((2, 0, 1))).float()
    msk = torch.from_numpy(msk.transpose((2, 0, 1)).copy()).long()
    nadir = torch.from_numpy(np.asarray([(nadir / 60.0)]).copy()).float()
    cat_inp = torch.from_numpy(cat_inp.copy()).float()
    coord_inp = torch.from_numpy(coord_inp.copy()).float()
    sample = {'img': img, 'mask': msk, 'nadir': nadir, 'cat_inp': cat_inp, 'coord_inp': coord_inp, 'img_name': fn}
    return sample
