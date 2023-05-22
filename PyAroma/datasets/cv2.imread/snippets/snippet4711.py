from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import numpy as np
from sklearn.model_selection import train_test_split, KFold
import cv2


def get_training_list(root_folder=TRAIN_ROOT, count_label=True):
    dict_list = {}
    basname = [img_basename(f) for f in os.listdir(os.path.join(root_folder, 'images/nir'))]
    if count_label:
        for key in labels_folder.keys():
            no_zero_files = []
            for fname in basname:
                gt = np.array(cv2.imread(os.path.join(root_folder, 'labels', key, (fname + '.png')), (- 1)))
                if np.count_nonzero(gt):
                    no_zero_files.append(fname)
                else:
                    continue
            dict_list[key] = no_zero_files
    return (dict_list, basname)
