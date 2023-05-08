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
def evaluating(h, model, test_x, test_y):
    print('[INFO] evaluating network...')
    predictions = model.predict(test_x, batch_size=size)
    print(classification_report(test_y.argmax(axis=1), predictions.argmax(axis=1), target_names=['EOSINOPHIL', 'LYMPHOCYTE', 'MONOCYTE', 'NEUTROPHIL']))
    Learning.show_plot(h)
