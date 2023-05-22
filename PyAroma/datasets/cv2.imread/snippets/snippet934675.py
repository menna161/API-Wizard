import os
import glob
import traceback
import collections
import sys
import math
import copy
import json
import random
import numpy as np
import torch
import cv2
from torch.utils.data import Dataset
from . import splitter
from . import data_parser
from configs import g_conf
from coilutils.general import sort_nicely


def __getitem__(self, index):
    '\n        Get item function used by the dataset loader\n        returns all the measurements with the desired image.\n\n        Args:\n            index:\n\n        Returns:\n\n        '
    try:
        img_path = os.path.join(self.root_dir, self.sensor_data_names[index].split('/')[(- 2)], self.sensor_data_names[index].split('/')[(- 1)])
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if (self.transform is not None):
            boost = 1
            img = self.transform((self.batch_read_number * boost), img)
        else:
            img = img.transpose(2, 0, 1)
        img = img.astype(np.float)
        img = torch.from_numpy(img).type(torch.FloatTensor)
        img = (img / 255.0)
        measurements = self.measurements[index].copy()
        for (k, v) in measurements.items():
            v = torch.from_numpy(np.asarray([v]))
            measurements[k] = v.float()
        measurements['rgb'] = img
        self.batch_read_number += 1
    except AttributeError:
        print('Blank IMAGE')
        measurements = self.measurements[0].copy()
        for (k, v) in measurements.items():
            v = torch.from_numpy(np.asarray([v]))
            measurements[k] = v.float()
        measurements['steer'] = 0.0
        measurements['throttle'] = 0.0
        measurements['brake'] = 0.0
        measurements['rgb'] = np.zeros(3, 88, 200)
    return measurements
