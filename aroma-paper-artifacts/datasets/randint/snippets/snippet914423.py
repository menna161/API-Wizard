from keras.models import load_model
from CNN.preprocessing import ImageToArray
from CNN.preprocessing import PreProcessor
from CNN.datasets.DatasetLoader import DatasetLoader
import matplotlib.pyplot as plt
import numpy as np
import argparse
from imutils import paths
import cv2


def sampling_images():
    print('[INFO] sampling images ...')
    image_paths = np.array(list(paths.list_images(args['dataset'])))
    idxs = np.random.randint(0, len(image_paths), size=(10,))
    image_paths = image_paths[idxs]
    sp = PreProcessor.PreProcessor(size, size)
    iap = ImageToArray.ImageToArrayPreprocessor()
    sdl = DatasetLoader(preprocessors=[sp, iap])
    (data, labels) = sdl.load(image_paths)
    data = (data.astype('float') / 255.0)
    return (data, image_paths)
