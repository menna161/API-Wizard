import sys
import cv2
import os
import csv
import numpy as np
import utils.visualize as visualize
from multiprocessing import Pool
from cv2.dnn import NMSBoxes
from scipy.ndimage.measurements import label
import scipy.ndimage as ndimage
import copy
from gtdb import fit_box
from gtdb import box_utils
from gtdb import feature_extractor
import shutil
import time
from collections import OrderedDict
from collections import deque
import argparse


def adjust_char(params):
    '\n    Adjust the character bounding boxes\n    '
    try:
        (args, char_regions, pdf_name, page_num) = params
        print('Char processing ', pdf_name, ' > ', page_num)
        image = cv2.imread(os.path.join(args.home_images, pdf_name, (str((int(page_num) + 1)) + '.png')))
        im_bw = fit_box.convert_to_binary(image)
        new_chars = []
        for char in char_regions:
            bb_char = [char[2], char[3], char[4], char[5]]
            bb_char = [int(float(k)) for k in bb_char]
            box = fit_box.adjust_box(im_bw, bb_char)
            if ((feature_extractor.width(box) > 0) and (feature_extractor.height(box) > 0)):
                char[1] = box[0]
                char[2] = box[1]
                char[3] = box[2]
                char[4] = box[3]
                new_chars.append(char)
        return new_chars
    except Exception as e:
        print('Error while processing ', pdf_name, ' > ', page_num, sys.exc_info())
        return []
