from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import keras
from keras.callbacks import ModelCheckpoint, LambdaCallback
from keras.optimizers import RMSprop, SGD, Adam
import numpy as np
import argparse
import os
from os import path
import time
import matplotlib.image as img
import matplotlib.pyplot as plt
from scipy import misc
from densemapnet import Settings
from densemapnet import DenseMapNet
from keras import objectives
from keras import backend as K
import tensorflow as tf
import tifffile


def get_epe(self, use_train_data=True, get_performance=False):
    if use_train_data:
        lx = self.train_lx
        rx = self.train_rx
        dx = self.train_dx
        if self.settings.mask:
            print('Using mask images')
            mx = self.train_mx
        print('Using train data... Size: ', lx.shape[0])
    else:
        lx = self.test_lx
        rx = self.test_rx
        dx = self.test_dx
        if self.settings.mask:
            print('Using mask images')
            mx = self.test_mx
        if self.settings.predict:
            print('Using complete data... Size: ', lx.shape[0])
        else:
            print('Using test data... Size: ', lx.shape[0])
    epe_total = 0
    my3pe_total = 0
    t = 0
    nsamples = lx.shape[0]
    elapsed_total = 0.0
    if self.settings.images:
        print('Saving images on folder...')
    for i in range(0, nsamples, 1):
        indexes = np.arange(i, (i + 1))
        left_images = lx[(indexes, :, :, :)]
        right_images = rx[(indexes, :, :, :)]
        disparity_images = dx[(indexes, :, :, :)]
        if self.settings.mask:
            mask_images = mx[(indexes, :, :, :)]
        if get_performance:
            start_time = time.time()
            predicted_disparity = self.model.predict([left_images, right_images])
            elapsed_total += (time.time() - start_time)
        else:
            predicted_disparity = self.model.predict([left_images, right_images])
        predicted = predicted_disparity[(0, :, :, :)]
        ground = disparity_images[(0, :, :, :)]
        if self.settings.mask:
            ground_mask = mask_images[(0, :, :, :)]
            dim = np.count_nonzero(ground_mask)
            nz = np.nonzero(ground_mask)
            epe = (predicted[nz] - ground[nz])
        else:
            dim = (predicted.shape[0] * predicted.shape[1])
            epe = (predicted - ground)
        mask = (ground != NO_DATA)
        epe = epe[mask]
        dim = len(epe)
        mask = (ground == NO_DATA)
        ground[mask] = 0
        my3pe = np.sum((np.absolute(epe) < 3.0))
        my3pe = my3pe.astype('float32')
        my3pe = (my3pe / dim)
        my3pe_total += my3pe
        epe = np.sum(np.absolute(epe))
        epe = epe.astype('float32')
        epe = (epe / dim)
        epe_total += epe
        if ((get_performance and self.settings.images) or ((i % 1) == 0)):
            path = 'test'
            if use_train_data:
                path = 'train'
            filepath = os.path.join(self.images_pdir, path)
            left = os.path.join(filepath, 'left')
            right = os.path.join(filepath, 'right')
            disparity = os.path.join(filepath, 'disparity')
            prediction = os.path.join(filepath, 'prediction')
            filename = ('%04d.png' % i)
            tiffname = ('%04d.tif' % i)
            left = os.path.join(left, filename)
            self.save_rgb_image(left_images[0], left)
            right = os.path.join(right, filename)
            self.save_rgb_image(right_images[0], right)
            self.save_disparity_image(predicted, os.path.join(prediction, tiffname))
            self.save_disparity_image(ground, os.path.join(disparity, tiffname))
    epe = (epe_total / nsamples)
    tpe = (1.0 - (my3pe_total / nsamples))
    if (self.settings.dataset == 'kitti2015'):
        epe = (epe / 256.0)
        print('KITTI 2015 EPE: ', epe)
    else:
        print(('EPE: %0.2fpix' % epe))
        print(('3PE: %0.2f' % tpe))
    if (epe < self.best_epe):
        self.best_epe = epe
        print(('------------------- BEST EPE : %f ---------------------' % epe))
        tmpdir = 'tmp'
        try:
            os.mkdir(tmpdir)
        except FileExistsError:
            print('Folder exists: ', tmpdir)
        filename = open('tmp\\epe.txt', 'a')
        datetime = time.strftime('%H:%M:%S')
        filename.write(('%s : LR: %f : %s EPE: %f 3PE: %f\n' % (datetime, self.settings.lr, self.settings.dataset, epe, tpe)))
        filename.close()
    if get_performance:
        print(('Speed: %0.4fsec' % (elapsed_total / nsamples)))
        print(('Speed: %0.4fHz' % (nsamples / elapsed_total)))
