import collections
import colorsys
import logging
import queue
import signal
import sys
from argparse import ArgumentParser
from datetime import datetime
import cv2
import numpy as np
import capture_conf
from deep_sort import nn_matching
from deep_sort import preprocessing
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from lffd.lffd import Predict
from util.cost import Cost
from util.source_queue import SourceQueue
from util.threadpoolutils import submit, new_pools
import os
from mxnet import context


def test(self):
    for i in range(1, 9):
        im = cv2.imread('/home/lijc08/桌面/{}.jpg'.format(i))
        now = datetime.now()
        (bboxes, feature) = self.detector.predict(im, score_threshold=self.conf.score_threshold, top_k=self.conf.top_k, NMS_threshold=self.conf.NMS_threshold)
        print('cost:{} sec'.format((datetime.now() - now).total_seconds()))
        for bbox in bboxes:
            cv2.rectangle(im, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        if (max(im.shape[:2]) > 1440):
            scale = (1440 / max(im.shape[:2]))
            im = cv2.resize(im, (0, 0), fx=scale, fy=scale)
        cv2.imshow('im', im)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
