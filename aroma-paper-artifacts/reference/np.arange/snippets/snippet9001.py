from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os.path
import re
import sys
import random
import tarfile
import scipy.misc
import re
from tensorflow.contrib.keras.api.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from six.moves import urllib
import tensorflow as tf
from fnmatch import fnmatch


def __init__(self, data_path, targetFile=None, targetClass=None):
    if (targetFile is None):
        random.seed(5566)
        from fnmatch import fnmatch
        file_list = []
        for (path, subdirs, files) in os.walk(data_path):
            for name in files:
                if fnmatch(name, '*.jpg'):
                    file_list.append(os.path.join(path, name))
        random.shuffle(file_list)
        FILENAME_RE = re.compile('(\\d+).(\\d+).jpg')
        temp_data = []
        temp_labels = []
        for f in file_list:
            img = scipy.misc.imread(f)
            if ((img.shape[0] < 299) or (img.shape[1] < 299)):
                continue
            img = ((np.array(scipy.misc.imresize(img, (299, 299)), dtype=np.float32) / 255) - 0.5)
            if (img.shape != (299, 299, 3)):
                continue
            img = np.expand_dims(img, axis=0)
            temp_data.append(img)
            filename_search = FILENAME_RE.search(f)
            temp_labels.append(int(filename_search.group(1)))
        data_num = len(temp_data)
        print('Imagenet load # testing images:{}'.format(data_num))
        temp_data = np.concatenate(temp_data)
        temp_labels = np.array(temp_labels)
        self.test_data = temp_data
        self.test_labels = np.zeros((data_num, 1001))
        self.test_labels[(np.arange(data_num), temp_labels)] = 1
    else:
        print('Target file:{}'.format(targetFile))
        (temp_data, temp_label) = readimg(targetFile, force=True)
        self.test_data = np.array(temp_data)
        temp_label = np.array(temp_label)
        self.test_labels = np.zeros((1, 1001))
        self.test_labels[(0, temp_label)] = 1
        print('Read target file {}'.format(targetFile))
