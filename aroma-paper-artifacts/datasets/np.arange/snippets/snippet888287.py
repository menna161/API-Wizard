from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.utils.data_utils import get_file
from tensorflow.python.keras.datasets.cifar import load_batch
from capslayer.data.utils.TFRecordHelper import int64_feature, bytes_feature


def load_cifar100(split, path=None):
    if (path is None):
        cache_path = os.path.join(os.path.expanduser('~'), '.capslayer')
        path = get_file('cifar-100-python', cache_dir=cache_path, file_hash=md5sum, origin=URL, untar=True)
    split = split.lower()
    if (split == 'test'):
        fpath = os.path.join(path, 'test')
        (images, labels) = load_batch(fpath, label_key='fine_labels')
    else:
        fpath = os.path.join(path, 'train')
        (images, labels) = load_batch(fpath, label_key='fine_labels')
        idx = np.arange(len(images))
        np.random.seed(201808)
        np.random.shuffle(idx)
        labels = np.reshape(labels, ((- 1),))
        images = (images[idx[:45000]] if (split == 'train') else images[idx[45000:]])
        labels = (labels[idx[:45000]] if (split == 'train') else labels[idx[45000:]])
    images = np.reshape(images.transpose(0, 2, 3, 1), ((- 1), 3072)).astype(np.float32)
    labels = np.reshape(labels, ((- 1),)).astype(np.int32)
    return zip(images, labels)
