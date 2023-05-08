import os
import cv2
import json
import random
from collections import defaultdict
import panda_utils as util


def loadImg(self, imgpath):
    '\n        :param imgpath: the path of image to load\n        :return: loaded img object\n        '
    print('filename:', imgpath)
    if (not os.path.exists(imgpath)):
        print('Can not find {}, please check local dataset!'.format(imgpath))
        return None
    img = cv2.imread(imgpath)
    (imgheight, imgwidth) = img.shape[:2]
    scale = (self.showwidth / imgwidth)
    img = cv2.resize(img, (int((imgwidth * scale)), int((imgheight * scale))))
    return img
