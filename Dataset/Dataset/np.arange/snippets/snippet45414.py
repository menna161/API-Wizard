from .config import HOME
import os.path as osp
import sys
import torch
import torch.utils.data as data
import cv2
import numpy as np
from gtdb import box_utils
from gtdb import feature_extractor
import copy
import utils.visualize as visualize


def generate_metadata(self):
    for id in self.ids:
        math_patches = []
        (height, width, channels) = self.images[id[1]].shape
        current_page_boxes = self.math_ground_truth[id[1]]
        n_horizontal = np.ceil((width / self.window))
        n_vertical = np.ceil((height / self.window))
        h = np.arange(0, ((n_horizontal - 1) + self.stride), self.stride)
        v = np.arange(0, ((n_vertical - 1) + self.stride), self.stride)
        crop_size = self.window
        if (((self.split == 'train') or (self.split == 'validate')) and self.is_math[id[1]]):
            for i in h:
                for j in v:
                    x_l = int(np.round((crop_size * i)))
                    x_h = (x_l + self.window)
                    y_l = int(np.round((crop_size * j)))
                    y_h = (y_l + self.window)
                    image_box = [x_l, y_l, x_h, y_h]
                    current_page_boxes = copy.deepcopy(self.math_ground_truth[id[1]])
                    for box in current_page_boxes:
                        if box_utils.intersects(image_box, box):
                            box[0] = max(x_l, box[0])
                            box[1] = max(y_l, box[1])
                            box[2] = min(x_h, box[2])
                            box[3] = min(y_h, box[3])
                            box[0] = (box[0] - x_l)
                            box[2] = (box[2] - x_l)
                            box[1] = (box[1] - y_l)
                            box[3] = (box[3] - y_l)
                            if ((feature_extractor.width(box) > 0) and (feature_extractor.height(box) > 0)):
                                self.metadata.append([id[1], x_l, y_l])
                                break
        elif (self.split == 'test'):
            for i in h:
                for j in v:
                    x_l = int(np.round((crop_size * i)))
                    y_l = int(np.round((crop_size * j)))
                    self.metadata.append([id[1], x_l, y_l])
