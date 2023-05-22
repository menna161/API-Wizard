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
    if (img2 is None):
        print('Error!', fn)
    img3 = cv2.imread(path.join(train_dir3, fn), cv2.IMREAD_COLOR)
    msk = cv2.imread(path.join(masks_folder, fn), cv2.IMREAD_COLOR)
    occluded_msk = cv2.imread(path.join(occluded_masks_dir, fn), cv2.IMREAD_UNCHANGED)
    if (random.random() > 0.8):
        shift_pnt = (random.randint((- 400), 400), random.randint((- 400), 400))
        img = shift_image(img, shift_pnt)
        img2 = shift_image(img2, shift_pnt)
        img3 = shift_image(img3, shift_pnt)
        msk = shift_image(msk, shift_pnt)
        occluded_msk = shift_image(occluded_msk, shift_pnt)
    if (random.random() > 0.9):
        rot_pnt = (((img.shape[0] // 2) + random.randint((- 150), 150)), ((img.shape[1] // 2) + random.randint((- 150), 150)))
        scale = 1
        angle = (random.randint(0, 8) - 4)
        if ((angle != 0) or (scale != 1)):
            img = rotate_image(img, angle, scale, rot_pnt)
            img2 = rotate_image(img2, angle, scale, rot_pnt)
            img3 = rotate_image(img3, angle, scale, rot_pnt)
            msk = rotate_image(msk, angle, scale, rot_pnt)
            occluded_msk = rotate_image(occluded_msk, angle, scale, rot_pnt)
    crop_size = input_shape[0]
    if (random.random() > 0.85):
        crop_size = random.randint(int((input_shape[0] / 1.2)), int((input_shape[0] / 0.8)))
    x0 = random.randint(0, (img.shape[1] - crop_size))
    y0 = random.randint(0, (img.shape[0] - crop_size))
    img = img[(y0:(y0 + crop_size), x0:(x0 + crop_size), :)]
    img2 = img2[(y0:(y0 + crop_size), x0:(x0 + crop_size), :)]
    img3 = img3[(y0:(y0 + crop_size), x0:(x0 + crop_size), :)]
    msk = msk[(y0:(y0 + crop_size), x0:(x0 + crop_size), :)]
    occluded_msk = occluded_msk[(y0:(y0 + crop_size), x0:(x0 + crop_size), ...)]
    if (crop_size != input_shape[0]):
        img = cv2.resize(img, input_shape, interpolation=cv2.INTER_LINEAR)
        img2 = cv2.resize(img2, input_shape, interpolation=cv2.INTER_LINEAR)
        img3 = cv2.resize(img3, input_shape, interpolation=cv2.INTER_LINEAR)
        msk = cv2.resize(msk, input_shape, interpolation=cv2.INTER_LINEAR)
        occluded_msk = cv2.resize(occluded_msk, input_shape, interpolation=cv2.INTER_LINEAR)
    if (random.random() > 0.5):
        if (random.random() > 0.91):
            img = clahe(img)
            img2 = clahe(img2)
            img3 = clahe(img3)
        elif (random.random() > 0.91):
            img = gauss_noise(img)
            img2 = gauss_noise(img2)
            img3 = gauss_noise(img3)
        elif (random.random() > 0.91):
            img = cv2.blur(img, (3, 3))
            img2 = cv2.blur(img2, (3, 3))
            img3 = cv2.blur(img3, (3, 3))
    elif (random.random() > 0.91):
        img = saturation(img, (0.9 + (random.random() * 0.2)))
        img2 = saturation(img2, (0.9 + (random.random() * 0.2)))
        img3 = saturation(img3, (0.9 + (random.random() * 0.2)))
    elif (random.random() > 0.91):
        img = brightness(img, (0.9 + (random.random() * 0.2)))
        img2 = brightness(img2, (0.9 + (random.random() * 0.2)))
        img3 = brightness(img3, (0.9 + (random.random() * 0.2)))
    elif (random.random() > 0.91):
        img = contrast(img, (0.9 + (random.random() * 0.2)))
        img2 = contrast(img2, (0.9 + (random.random() * 0.2)))
        img3 = contrast(img3, (0.9 + (random.random() * 0.2)))
    if (random.random() > 0.96):
        el_det = self.elastic.to_deterministic()
        img = el_det.augment_image(img)
        img2 = el_det.augment_image(img2)
        img3 = el_det.augment_image(img3)
    msk = ((msk > 127) * 1)
    occluded_msk = ((occluded_msk > 127) * 1)
    occluded_msk = occluded_msk[(..., np.newaxis)]
    msk = np.concatenate([msk, occluded_msk], axis=2)
    img = np.concatenate([img, img2, img3], axis=2)
    img = preprocess_inputs(img)
    (nadir, cat_inp, coord_inp) = parse_img_id(fn)
    img = torch.from_numpy(img.transpose((2, 0, 1))).float()
    msk = torch.from_numpy(msk.transpose((2, 0, 1)).copy()).long()
    nadir = torch.from_numpy(np.asarray([(nadir / 60.0)]).copy()).float()
    cat_inp = torch.from_numpy(cat_inp.copy()).float()
    coord_inp = torch.from_numpy(coord_inp.copy()).float()
    sample = {'img': img, 'mask': msk, 'nadir': nadir, 'cat_inp': cat_inp, 'coord_inp': coord_inp, 'img_name': fn}
    return sample
