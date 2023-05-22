from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.utils.data_utils import get_file
from tensorflow.python.keras.datasets.cifar import load_batch
from capslayer.data.utils.TFRecordHelper import int64_feature, bytes_feature


def load_cifar10(split, path=None):
    if (path is None):
        cache_path = os.path.join(os.path.expanduser('~'), '.capslayer')
        path = get_file('cifar-10-batches-py', cache_dir=cache_path, file_hash=md5sum, origin=URL, untar=True)
    split = split.lower()
    if (split == 'test'):
        fpath = os.path.join(path, 'test_batch')
        (images, labels) = load_batch(fpath)
    else:
        num_samples = 50000
        images = np.empty((num_samples, 3, 32, 32), dtype='uint8')
        labels = np.empty((num_samples,), dtype='uint8')
        for i in range(1, 6):
            fpath = os.path.join(path, ('data_batch_' + str(i)))
            (images[(((i - 1) * 10000):(i * 10000), :, :, :)], labels[((i - 1) * 10000):(i * 10000)]) = load_batch(fpath)
        idx = np.arange(len(images))
        np.random.seed(201808)
        np.random.shuffle(idx)
        images = (images[idx[:45000]] if (split == 'train') else images[idx[45000:]])
        labels = (labels[idx[:45000]] if (split == 'train') else labels[idx[45000:]])
    images = np.reshape(images.transpose(0, 2, 3, 1), ((- 1), 3072)).astype(np.float32)
    labels = np.reshape(labels, ((- 1),)).astype(np.int32)
    return zip(images, labels)
