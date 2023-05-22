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


def find_contours(image, min_area=0, sort=True):
    image = image.copy()
    if (opencv_version() == 3):
        contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]
    else:
        contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    contours = [contour for contour in contours if (cv2.contourArea(contour) >= min_area)]
    if (len(contours) < 1):
        return ([], [])
    if sort:
        bndboxes = [cv2.boundingRect(contour) for contour in contours]
        (contours, bndboxes) = zip(*sorted(zip(contours, bndboxes), key=(lambda x: x[1][0])))
    return (contours, bndboxes)
