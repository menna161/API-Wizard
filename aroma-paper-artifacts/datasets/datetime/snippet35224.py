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


def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
