import sys
import cv2
import os
import numpy as np
from multiprocessing import Pool
from gtdb import fit_box
from gtdb import feature_extractor
import argparse


def normalize(params):
    (args, math_regions, pdf_name, page_num) = params
    print('Processing ', pdf_name, ' > ', page_num)
    image = cv2.imread(os.path.join(args.home_images, pdf_name, (str(int((page_num + 1))) + '.png')))
    im_bw = fit_box.convert_to_binary(image)
    new_math = []
    for math in math_regions:
        box = [(math[0] / im_bw.shape[1]), (math[1] / im_bw.shape[0]), (math[2] / im_bw.shape[1]), (math[3] / im_bw.shape[0])]
        if ((feature_extractor.width(box) > 0) and (feature_extractor.height(box) > 0)):
            new_math.append(box)
    return new_math
