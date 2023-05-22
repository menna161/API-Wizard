import base64
import datetime
import io
import json
import os
import time
import webbrowser
import colorama
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QFileDialog
from keras.models import model_from_json


def binarize(image, points=None, thresh=128, maxval=255, thresh_type=0):
    image = image.copy()
    if ((not (points is None)) and (type(points) is list) and (len(points) > 2)):
        points = sort_points(points)
        points = numpy.array(points, numpy.int64)
        mask = numpy.zeros_like(image, numpy.uint8)
        cv2.fillConvexPoly(mask, points, (255, 255, 255), cv2.LINE_AA)
        image = cv2.bitwise_and(image, mask)
    msers = cv2.MSER_create().detectRegions(image)[0]
    setyx = set()
    for region in msers:
        for point in region:
            setyx.add((point[1], point[0]))
    setyx = tuple(numpy.transpose(list(setyx)))
    mask1 = numpy.zeros(image.shape, numpy.uint8)
    mask1[setyx] = maxval
    mask2 = cv2.threshold(image, thresh, maxval, thresh_type)[1]
    image = cv2.bitwise_and(mask1, mask2)
    return image
