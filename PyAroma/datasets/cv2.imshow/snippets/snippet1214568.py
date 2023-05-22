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


def save_images(self, img, tracks):
    cost = Cost('save_images')
    for track in tracks:
        (frame_index, track_id) = (track[0], track[1])
        (x1, y1, x2, y2) = self.tlwh2rec(track[2])
        ret_img = img[(y1:y2, x1:x2, :)]
        if self.conf.is_async:
            self.save_pool.submit(cv2.imwrite, './save/images/{}_{}.jpg'.format(track_id, frame_index), ret_img)
        else:
            if self.debug:
                cv2.imshow('save', ret_img)
            cv2.imwrite('./save/images/{}_{}.jpg'.format(track_id, frame_index), ret_img)
    cost.end(logger.info, show=(True if self.debug else False))
