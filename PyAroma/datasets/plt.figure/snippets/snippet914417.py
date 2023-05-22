from keras.models import load_model
from CNN.preprocessing import ImageToArray
from CNN.preprocessing import PreProcessor
from CNN.datasets.DatasetLoader import DatasetLoader
import matplotlib.pyplot as plt
import numpy as np
import argparse
from imutils import paths
import cv2


def show(image):
    plt.figure(figsize=(15, 15))
    plt.imshow(image, interpolation='nearest')
    plt.show()
