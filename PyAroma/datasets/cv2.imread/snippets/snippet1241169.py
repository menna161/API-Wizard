import os
import json
import numpy as np
import pandas as pd
import glob
import cv2
import os
import shutil
from IPython import embed
from sklearn.model_selection import train_test_split


def _image(self, path):
    image = {}
    print(path)
    img = cv2.imread((self.image_dir + path))
    image['height'] = img.shape[0]
    image['width'] = img.shape[1]
    image['id'] = self.img_id
    image['file_name'] = path
    return image
