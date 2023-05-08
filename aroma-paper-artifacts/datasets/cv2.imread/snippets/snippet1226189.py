from __future__ import division
import os
import numpy as np
import cv2
from libs import utils
from torch.utils.data import Dataset
import json
from PIL import Image


def get_img_size(self):
    img = cv2.imread(os.path.join(self.db_root_dir, self.img_list[0]))
    return list(img.shape[:2])
