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
def show_plot(h):
    plt.style.use('ggplot')
    plt.figure()
    plt.plot(np.arange(0, ep), h.history['loss'], label='train_loss')
    plt.plot(np.arange(0, ep), h.history['val_loss'], label='val_loss')
    plt.plot(np.arange(0, ep), h.history['acc'], label='acc')
    plt.plot(np.arange(0, ep), h.history['val_acc'], label='val_acc')
    plt.title('AMINJAMAL')
    plt.xlabel('Epoch #')
    plt.ylabel('Loss/ACC')
    plt.legend()
    plt.show()
