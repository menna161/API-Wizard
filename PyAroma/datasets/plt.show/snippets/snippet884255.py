import os
import colorsys
import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from yolo4.model import yolo_eval, yolo4_body
from yolo4.utils import letterbox_image
from PIL import Image, ImageFont, ImageDraw
from timeit import default_timer as timer
import matplotlib.pyplot as plt

if (__name__ == '__main__'):
    model_path = 'yolo4_weight.h5'
    anchors_path = 'model_data/yolo4_anchors.txt'
    classes_path = 'model_data/coco_classes.txt'
    score = 0.5
    iou = 0.5
    model_image_size = (608, 608)
    yolo4_model = Yolo4(score, iou, anchors_path, classes_path, model_path)
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            result = yolo4_model.detect_image(image, model_image_size=model_image_size)
            plt.imshow(result)
            plt.show()
    yolo4_model.close_session()
