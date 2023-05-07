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


def video_on_sync(self):
    cost = Cost('video display')
    (im, bboxes, tracks) = self.box_queue.get()
    for bbox in bboxes:
        cv2.rectangle(im, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 1)
    cost.record('draw detect')
    if self.conf.track_on:
        for track in tracks:
            color = create_unique_color_uchar(track[1])
            (x1, y1, x2, y2) = self.tlwh2rec(track[2])
            cv2.rectangle(im, (x1, y1), (x2, y2), color, 2)
    cost.record('draw track')
    if (max(im.shape[:2]) > 1440):
        scale = (1440 / max(im.shape[:2]))
        im = cv2.resize(im, (0, 0), fx=scale, fy=scale)
    cv2.putText(im, (str(format(self.fps, '.2f')) + ' fps'), (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2, lineType=2)
    cv2.imshow('detect', im)
    cv2.waitKey(1)
    cost.end(func=logger.info, show=True)
