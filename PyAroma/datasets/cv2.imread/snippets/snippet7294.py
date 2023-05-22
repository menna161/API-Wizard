import tensorflow as tf
import numpy as np
import cv2
import glob
from tqdm import tqdm
import os


def load_custom_data_AE(datadir=None, img_shape=(64, 64)):
    'Loads train and test data from a specified directory and returns a numpy array of train and test images - used in Autoencoder\n\n    Args:\n        datadir (str): directory to load data from. Defaults to ``None``\n        img_shape (int, tuple, optional): shape of the image to be returned. Defaults to ``(64, 64)``\n\n    Return:\n        a numpy array of shape according to img_shape parameter\n    '
    assert (datadir is not None), 'Enter a valid directory'
    error_message = 'train directory not found \n Directory structure: \n {} \n {} -train \n {} -*.jpg \n {} -test \n {} -*.jpg'.format(datadir, (' ' * 2), (' ' * 4), (' ' * 2), (' ' * 4))
    assert os.path.exists(os.path.join(datadir, 'train')), error_message
    error_message = 'test directory not found \n Directory structure: \n {} \n {} -train \n {} -*.jpg \n {} -test \n {} -*.jpg'.format(datadir, (' ' * 2), (' ' * 4), (' ' * 2), (' ' * 4))
    assert os.path.exists(os.path.join(datadir, 'test')), error_message
    assert ((len(img_shape) == 2) and isinstance(img_shape, tuple)), 'img_shape must be a tuple of size 2'
    train_data = []
    files = glob.glob(os.path.join(datadir, 'train/*'))
    for file in tqdm(files, desc='Loading train images'):
        try:
            image = cv2.imread(file)
            image = cv2.resize(image, img_shape, interpolation=cv2.INTER_AREA)
            train_data.append(image)
        except BaseException:
            print('Error: Unable to load an image from directory')
            pass
    assert (len(train_data) > 0), 'No images to load from train directory'
    test_data = []
    files = glob.glob(os.path.join(datadir, 'test/*'))
    for file in tqdm(files, desc='Loading test images'):
        try:
            image = cv2.imread(file)
            image = cv2.resize(image, img_shape, interpolation=cv2.INTER_AREA)
            test_data.append(image)
        except BaseException:
            print('Error: Unable to load an image from directory')
            pass
    assert (len(test_data) > 0), 'No images to load from test directory'
    train_data = np.array(train_data).astype('float32')
    test_data = np.array(test_data).astype('float32')
    return (train_data, test_data)
