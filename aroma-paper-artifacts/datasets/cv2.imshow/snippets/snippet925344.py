import torch
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from models import EfficientDet
from torchvision import transforms
import numpy as np
import skimage
from datasets import get_augumentation, VOC_CLASSES
from timeit import default_timer as timer
import argparse
import copy
from utils import vis_bbox, EFFICIENTDET


def camera(self):
    cap = cv2.VideoCapture(0)
    if (not cap.isOpened()):
        print('Unable to open camera')
        exit((- 1))
    count_tfps = 1
    accum_time = 0
    curr_fps = 0
    fps = 'FPS: ??'
    prev_time = timer()
    while True:
        (res, img) = cap.read()
        curr_time = timer()
        exec_time = (curr_time - prev_time)
        prev_time = curr_time
        accum_time = (accum_time + exec_time)
        curr_fps = (curr_fps + 1)
        if (accum_time > 1):
            accum_time = (accum_time - 1)
            fps = curr_fps
            curr_fps = 0
        if res:
            show_image = self.process(img=img)
            cv2.putText(show_image, ('FPS: ' + str(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (204, 51, 51), 2)
            cv2.imshow('Detection', show_image)
            k = cv2.waitKey(1)
            if (k == 27):
                break
        else:
            print('Unable to read image')
            exit((- 1))
        count_tfps += 1
    cap.release()
    cv2.destroyAllWindows()
