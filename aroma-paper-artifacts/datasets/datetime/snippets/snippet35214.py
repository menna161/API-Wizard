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


def image2tensor(image, shape, padding=0.0, rescale=1.0, color_mode=None):
    output = (cv2.cvtColor(image, color_mode) if color_mode else image.copy())
    output = numpy.atleast_3d(output)
    rect_w = output.shape[1]
    rect_h = output.shape[0]
    sqrlen = int(numpy.ceil(((1.0 + padding) * max(rect_w, rect_h))))
    sqrbox = numpy.zeros((sqrlen, sqrlen, output.shape[2]), numpy.uint8)
    rect_x = ((sqrlen - rect_w) // 2)
    rect_y = ((sqrlen - rect_h) // 2)
    sqrbox[(rect_y:(rect_y + rect_h), rect_x:(rect_x + rect_w))] = output
    output = cv2.resize(sqrbox, shape[:2])
    output = numpy.atleast_3d(output)
    output = (numpy.asarray(output, numpy.float32) * rescale)
    output = output.reshape(((1,) + output.shape))
    return output
