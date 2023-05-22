import cv2
import h5py
import numpy as np
import pyexr
import open3d
import os
import sys
from io import BytesIO
from config import cfg
import mc


@classmethod
def _read_img(cls, file_path):
    if (mc_client is None):
        return (cv2.imread(file_path, cv2.IMREAD_UNCHANGED) / 255.0)
    else:
        pyvector = mc.pyvector()
        mc_client.Get(file_path, pyvector)
        buf = mc.ConvertBuffer(pyvector)
        img_array = np.frombuffer(buf, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
        return (img / 255.0)
