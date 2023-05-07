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


def grab_region(image, bwmask, contours, bndboxes, index):
    region = numpy.zeros_like(bwmask, numpy.uint8)
    if ((len(contours) > 0) and (len(bndboxes) > 0) and (index >= 0)):
        (x, y, w, h) = bndboxes[index]
        region = cv2.drawContours(region, contours, index, (255, 255, 255), (- 1), cv2.LINE_AA)
        region = region[(y:(y + h), x:(x + w))]
        bwmask = bwmask[(y:(y + h), x:(x + w))]
        bwmask = cv2.bitwise_and(region, region, mask=bwmask)
        region = image[(y:(y + h), x:(x + w))]
        region = cv2.bitwise_and(region, region, mask=bwmask)
    return region
