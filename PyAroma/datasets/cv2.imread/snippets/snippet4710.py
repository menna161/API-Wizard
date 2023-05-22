from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import numpy as np
from sklearn.model_selection import train_test_split, KFold
import cv2


def prepare_gt(root_folder=TRAIN_ROOT, out_path='gt'):
    if (not os.path.exists(os.path.join(root_folder, out_path))):
        print('----------creating groundtruth data for training./.val---------------')
        check_mkdir(os.path.join(root_folder, out_path))
        basname = [img_basename(f) for f in os.listdir(os.path.join(root_folder, 'images/rgb'))]
        gt = (basname[0] + '.png')
        for fname in basname:
            gtz = np.zeros((512, 512), dtype=int)
            for key in labels_folder.keys():
                gt = (fname + '.png')
                mask = (np.array((cv2.imread(os.path.join(root_folder, 'labels', key, gt), (- 1)) / 255), dtype=int) * labels_folder[key])
                gtz[(gtz < 1)] = mask[(gtz < 1)]
            for key in ['boundaries', 'masks']:
                mask = np.array((cv2.imread(os.path.join(root_folder, key, gt), (- 1)) / 255), dtype=int)
                gtz[(mask == 0)] = 255
            cv2.imwrite(os.path.join(root_folder, out_path, gt), gtz)
