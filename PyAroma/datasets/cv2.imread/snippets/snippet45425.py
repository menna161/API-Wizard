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


def adjust(params):
    '\n    Fit the bounding boxes to the characters\n    '
    (args, math_regions, pdf_name, page_num) = params
    print('Processing ', pdf_name, ' > ', page_num)
    image = cv2.imread(os.path.join(args.home_images, pdf_name, (str(int((page_num + 1))) + '.png')))
    im_bw = fit_box.convert_to_binary(image)
    new_math = []
    for math in math_regions:
        box = fit_box.adjust_box(im_bw, math)
        if ((feature_extractor.width(box) > 0) and (feature_extractor.height(box) > 0)):
            new_math.append(box)
    return new_math
