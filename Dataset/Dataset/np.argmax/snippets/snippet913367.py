import os
import time
import logging
import argparse
import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.nn.functional as F
import torch.nn.parallel
import torch.utils.data
from util import dataset, transform, config
from util.util import AverageMeter, intersectionAndUnion, check_makedirs, colorize
from model.pspnet import PSPNet
from model.pyconvsegnet import PyConvSegNet


def test(test_loader, data_list, model, classes, mean, std, base_size, crop_h, crop_w, scales, gray_folder, color_folder, colors):
    logger.info('>>>>>>>>>>>>>>>> Start Evaluation >>>>>>>>>>>>>>>>')
    data_time = AverageMeter()
    batch_time = AverageMeter()
    model.eval()
    end = time.time()
    for (i, (input, _)) in enumerate(test_loader):
        data_time.update((time.time() - end))
        input = np.squeeze(input.numpy(), axis=0)
        image = np.transpose(input, (1, 2, 0))
        (h, w, _) = image.shape
        if (base_size == 0):
            base_size = max(h, w)
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
        prediction /= len(scales)
        prediction = np.argmax(prediction, axis=2)
        batch_time.update((time.time() - end))
        end = time.time()
        if ((((i + 1) % 10) == 0) or ((i + 1) == len(test_loader))):
            logger.info('Test: [{}/{}] Data {data_time.val:.3f} ({data_time.avg:.3f}) Batch {batch_time.val:.3f} ({batch_time.avg:.3f}).'.format((i + 1), len(test_loader), data_time=data_time, batch_time=batch_time))
        check_makedirs(gray_folder)
        check_makedirs(color_folder)
        gray = np.uint8(prediction)
        color = colorize(gray, colors)
        (image_path, _) = data_list[i]
        image_name = image_path.split('/')[(- 1)].split('.')[0]
        gray_path = os.path.join(gray_folder, (image_name + '.png'))
        color_path = os.path.join(color_folder, (image_name + '.png'))
        cv2.imwrite(gray_path, gray)
        color.save(color_path)
    logger.info('<<<<<<<<<<<<<<<<< End Evaluation <<<<<<<<<<<<<<<<<')
