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


def post_processor(arg):
    (img_queue, arg_visualize) = arg
    while True:
        if (not img_queue.empty()):
            (x, seg_pred, exist_pred) = img_queue.get()
            seg_pred = seg_pred.numpy()[0]
            exist_pred = exist_pred.numpy()
            exist = [(1 if (exist_pred[(0, i)] > 0.5) else 0) for i in range(4)]
            print(exist)
            for i in getLane.prob2lines_CULane(seg_pred, exist):
                print(i)
            if arg_visualize:
                frame = x.squeeze().permute(1, 2, 0).numpy()
                img = visualize(frame, seg_pred, exist_pred)
                cv2.imshow('input_video', frame)
                cv2.imshow('output_video', img)
            if ((cv2.waitKey(1) & 255) == ord('q')):
                break
        else:
            pass
