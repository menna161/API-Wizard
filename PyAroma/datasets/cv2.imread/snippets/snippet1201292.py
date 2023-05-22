import os
from os import path, makedirs
import numpy as np
import random
import timeit
import cv2
import pandas as pd
from multiprocessing import Pool


def process_image(fid):
    fid = (fid + '.png')
    used_msks = []
    for pr_f in pred_folders:
        msk1 = cv2.imread(path.join('/wdata/', pr_f, '{0}.png'.format(fid.split('.')[0])), cv2.IMREAD_UNCHANGED)
        used_msks.append(msk1)
    msk = np.zeros_like(used_msks[0], dtype='float')
    for i in range(len(pred_folders)):
        p = used_msks[i]
        msk += (coefs[i] * p.astype('float'))
    msk /= np.sum(coefs)
    cv2.imwrite(path.join('/wdata/merged_oof', fid), msk.astype('uint8'), [cv2.IMWRITE_PNG_COMPRESSION, 9])
