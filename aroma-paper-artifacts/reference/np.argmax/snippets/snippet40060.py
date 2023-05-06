import cv2
import argparse
import numpy as np
from keras.callbacks import ModelCheckpoint, LambdaCallback
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras import backend as K
import tensorflow as tf
import time
import os
from scipy import misc
from model_icnet import build_icnet
import memory_saving_gradients


def predict_and_report_accuracy(self, rgb_images, truth_images):
    height = rgb_images[0].shape[0]
    width = rgb_images[0].shape[1]
    num = len(rgb_images)
    elapsed_total = 0.0
    max_category = (self.n_classes - 1)
    tps = np.zeros(max_category)
    tns = np.zeros(max_category)
    fps = np.zeros(max_category)
    fns = np.zeros(max_category)
    for i in range(num):
        start_time = time.time()
        indexes = np.arange(i, (i + 1))
        rgb = rgb_images[(indexes, :, :, :)]
        prediction = self.model.predict(rgb)
        prediction = prediction[0]
        if (prediction.shape[0] == 1):
            prediction = prediction.reshape(prediction.shape[1], prediction.shape[2], prediction.shape[3])
        elapsed_total += (time.time() - start_time)
        truth = truth_images[(i, :, :)]
        labels = np.zeros((height, width))
        for i in range(max_category):
            pred = np.argmax(prediction[(:, :, 0:max_category)], axis=2)
            pred = cv2.resize(pred, (height, width), interpolation=cv2.INTER_NEAREST)
            labels = pred
            self.update_stats(labels, truth, tps, fps, fns, max_category)
        if self.args.save_images:
            self.save_image(i, (rgb[0] * 255), truth, labels)
    mIoU = 0.0
    for j in range(max_category):
        iou = (tps[j] / ((tps[j] + fps[j]) + fns[j]))
        print(('  IoU: %0.4f' % iou))
        mIoU += iou
    mIoU /= max_category
    print(('mIoU: %0.4f' % mIoU))
    print(('Speed: %0.4f seconds' % (elapsed_total / num)))
    print(('Speed: %0.4f Hz' % (num / elapsed_total)))
    print(' ')
    if (mIoU > self.best_mIoU):
        self.best_mIoU = mIoU
        print('-------- BEST mIoU = ', mIoU, '--------')
        tmpdir = 'tmp'
        try:
            os.mkdir(tmpdir)
        except FileExistsError:
            print('Folder exists: ', tmpdir)
        filename = open('tmp/miou.txt', 'a')
        datetime = time.strftime('%H:%M:%S')
        for j in range(max_category):
            iou = (tps[j] / ((tps[j] + fps[j]) + fns[j]))
            filename.write(('  IoU: %0.4f\n' % iou))
        filename.write(('%s : mIoU: %f : Speed (Hz): %f\n' % (datetime, mIoU, (num / elapsed_total))))
        filename.close()
    else:
        print('Best was mIoU = ', self.best_mIoU)
