import random
from pathlib import Path
from socket import AF_INET, SOCK_DGRAM, socket, timeout
import cv2
import numpy as np
import pandas as pd
from PIL import Image


def display_img(window_name, img_path, screen_width, screen_height, i):
    'Display an image on the screen, overlaid on a black background.\n\n    Args:\n        window_name (str): name of OpenCV window\n        img_path (Path): local path to image to load and display\n        screen_width (int): width (in px) of the screen\n        screen_height (int): height (in px) of the screen\n        i (int): the index of the image\n\n    '
    print(f'[{i}]: Showing image {str(img_path)}...')
    img = Image.open(str(img_path)).convert('RGB')
    img = add_background(img, screen_width, screen_height)
    img = np.array(img)[(..., ::(- 1))]
    cv2.imshow(window_name, img)
