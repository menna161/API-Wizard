from keras.models import load_model
from CNN.preprocessing import ImageToArray
from CNN.preprocessing import PreProcessor
from CNN.datasets.DatasetLoader import DatasetLoader
import matplotlib.pyplot as plt
import numpy as np
import argparse
from imutils import paths
import cv2


def predicting(data, image_paths, model):
    preds = model.predict(data, batch_size=size).argmax(axis=1)
    print(preds)
    for (i, imagePath) in enumerate(image_paths):
        image = cv2.imread(imagePath)
        cv2.putText(image, 'Label: {}'.format(classLabels[preds[i]]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('Image', image)
        cv2.waitKey(0)
