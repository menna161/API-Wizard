import os
import cv2
import json
import copy
from collections import defaultdict


def loadImg(self, imgpath):
    '\n        :param imgpath: the path of image to load\n        :return: loaded img object\n        '
    print('filename:', imgpath)
    if (not os.path.exists(imgpath)):
        print('Can not find {}, please check local dataset!'.format(imgpath))
        return None
    img = cv2.imread(imgpath)
    return img
