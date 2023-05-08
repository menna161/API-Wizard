import tensorflow as tf
import numpy as np
import cv2
import glob
from tqdm import tqdm
import os


def load_custom_data(datadir=None, img_shape=(64, 64)):
    'Loads data from specified directory and returns a numpy array - used in GANs\n\n    Args:\n        datadir (str): directory to load data from. Defaults to ``None``\n        img_shape (int, tuple, optional): shape of the image to be returned. Defaults to ``(64, 64)``\n\n    Return:\n        a numpy array of shape according to img_shape parameter\n    '
    error_message = 'Enter a valid directory \n Directory structure: \n {} \n {} -*jpg'.format(datadir, (' ' * 2))
    assert (datadir is not None), error_message
    assert ((len(img_shape) == 2) and isinstance(img_shape, tuple)), 'img_shape must be a tuple of size 2'
    train_data = []
    files = glob.glob(os.path.join(datadir, '*'))
    for file in tqdm(files, desc='Loading images'):
        try:
            image = cv2.imread(file)
            image = cv2.resize(image, img_shape, interpolation=cv2.INTER_AREA)
            train_data.append(image)
        except BaseException:
            print('Error: Unable to load an image from directory')
            pass
    assert (len(train_data) > 0), 'No images to load from directory'
    train_data = np.array(train_data).astype('float32')
    return train_data
