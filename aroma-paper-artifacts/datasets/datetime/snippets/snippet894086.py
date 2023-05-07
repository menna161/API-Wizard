from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import datetime
import os.path
import cv2
import numpy as np
from skimage.measure import compare_ssim
from src.utils import preprocess


def train(model, ims, real_input_flag, configs, itr):
    'Trains a model.'
    ims_list = np.split(ims, configs.n_gpu)
    cost = model.train(ims_list, configs.lr, real_input_flag, itr)
    if configs.reverse_input:
        ims_rev = np.split(ims[(:, ::(- 1))], configs.n_gpu)
        cost += model.train(ims_rev, configs.lr, real_input_flag, itr)
        cost = (cost / 2)
    if ((itr % configs.display_interval) == 0):
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ('itr: ' + str(itr)))
        print(('training loss: ' + str(cost)))
