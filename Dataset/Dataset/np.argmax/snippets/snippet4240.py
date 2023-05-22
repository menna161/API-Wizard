import argparse
import cv2
import torch
from model import SCNN
from model_ENET_SAD import ENet_SAD
from utils.prob2lines import getLane
from utils.transforms import *
import time
from multiprocessing import Process, JoinableQueue, SimpleQueue
from threading import Lock


def visualize(img, seg_pred, exist_pred):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    lane_img = np.zeros_like(img)
    color = np.array([[255, 125, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255]], dtype='uint8')
    coord_mask = np.argmax(seg_pred, axis=0)
    for i in range(0, 4):
        if (exist_pred[(0, i)] > 0.5):
            lane_img[(coord_mask == (i + 1))] = color[i]
    img = cv2.addWeighted(src1=lane_img, alpha=0.8, src2=img, beta=1.0, gamma=0.0)
    return img
