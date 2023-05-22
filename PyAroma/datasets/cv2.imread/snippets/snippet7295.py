import tensorflow as tf
import numpy as np
import cv2
import glob
from tqdm import tqdm
import os


def load_custom_data_with_labels(datadir=None, img_shape=(64, 64)):
    'Loads train with labels from a specified directory and returns a numpy array of train images and labels - used in CGAN\n\n    Args:\n        datadir (str): directory to load data from. Defaults to ``None``\n        img_shape (int, tuple, optional): shape of the image to be returned. Defaults to ``(64, 64)``\n\n    Return:\n        a numpy array of shape according to img_shape parameter\n    '
    assert (datadir is not None), 'Enter a valid directory'
    assert ((len(img_shape) == 2) and isinstance(img_shape, tuple)), 'img_shape must be a tuple of size 2'
    train_data = []
    labels = []
    files = glob.glob(os.path.join(datadir, '*/*'))
    for file in tqdm(files, desc='Loading images'):
        try:
            image = cv2.imread(file)
            image = cv2.resize(image, img_shape, interpolation=cv2.INTER_AREA)
            train_data.append(image)
            label_name = int(file.split('/')[(- 2)])
            labels.append(label_name)
        except ValueError:
            print('Ensure Directory is of following structure: \n {} \n {} -label 1(int type) \n {} -*.jpg \n {} -label 2(int type) \n {} -*.jpg \n {} ...'.format(datadir, (' ' * 2), (' ' * 4), (' ' * 2), (' ' * 4), (' ' * 2)))
            break
    assert (len(train_data) > 0), 'No images to load from directory'
    train_data = np.array(train_data).astype('float32')
    labels = np.array(labels)
    labels = labels.reshape(((- 1), 1))
    return (train_data, labels)
