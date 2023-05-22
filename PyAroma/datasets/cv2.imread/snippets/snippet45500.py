import sys
import cv2
import os
import numpy as np
from multiprocessing import Pool
from gtdb import feature_extractor
import argparse


def scale(params):
    try:
        (args, math_regions, pdf_name, page_num) = params
        print('Processing ', pdf_name, ' > ', page_num)
        image = cv2.imread(os.path.join(args.home_images, pdf_name, (str(int((page_num + 1))) + '.png')))
        height = image.shape[0]
        width = image.shape[1]
        new_math = []
        for math in math_regions:
            box = [0, 0, 0, 0]
            box[0] = ((math[0] * width) / 512)
            box[1] = ((math[1] * height) / 512)
            box[2] = ((math[2] * width) / 512)
            box[3] = ((math[3] * height) / 512)
            if ((feature_extractor.width(box) > 0) and (feature_extractor.height(box) > 0)):
                new_math.append(box)
        return new_math
    except Exception as e:
        print('Error while processing ', pdf_name, ' > ', page_num, sys.exc_info())
        return []
