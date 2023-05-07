from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from CNN.preprocessing import ImageToArray
from CNN.preprocessing.PreProcessor import PreProcessor
from CNN.datasets.DatasetLoader import DatasetLoader
from CNN.nn.conv import IncludeNet
from keras.optimizers import SGD
import matplotlib.pyplot as plt
import numpy as np
import argparse
from imutils import paths


@staticmethod
def loading_dataset():
    print('[INFO] loading Images')
    image_paths = list(paths.list_images(args['dataset']))
    sp = PreProcessor(size, size)
    iap = ImageToArray.ImageToArrayPreprocessor()
    sdl = DatasetLoader(preprocessors=[sp, iap])
    (data, labels) = sdl.load(image_paths, verbose=500)
    print(data)
    data = (data.astype('float') / 255.0)
    (train_x, test_x, train_y, test_y) = train_test_split(data, labels, test_size=0.25, random_state=42)
    train_y = LabelBinarizer().fit_transform(train_y)
    test_y = LabelBinarizer().fit_transform(test_y)
    return (test_x, test_y, train_x, train_y)
