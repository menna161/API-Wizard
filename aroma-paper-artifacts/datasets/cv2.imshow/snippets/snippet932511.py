from argparse import ArgumentParser
import airsimneurips as airsim
import cv2
import threading
import time
import utils
import numpy as np
import math
import numpy as np


def image_callback(self):
    request = [airsim.ImageRequest('fpv_cam', airsim.ImageType.Scene, False, False)]
    response = self.airsim_client_images.simGetImages(request)
    img_rgb_1d = np.fromstring(response[0].image_data_uint8, dtype=np.uint8)
    img_rgb = img_rgb_1d.reshape(response[0].height, response[0].width, 3)
    if self.viz_image_cv2:
        cv2.imshow('img_rgb', img_rgb)
        cv2.waitKey(1)
