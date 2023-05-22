import sys
import cv2
import os
import numpy as np
from multiprocessing import Pool
from cv2.dnn import NMSBoxes
from scipy.ndimage.measurements import label
from gtdb import fit_box
from gtdb import feature_extractor
import argparse
import shutil


def voting_algo(params):
    (args, math_regions, pdf_name, page_num) = params
    print('Processing ', pdf_name, ' > ', page_num)
    image = cv2.imread(os.path.join(args.home_images, pdf_name, (str(int((page_num + 1))) + '.png')))
    if args.preprocess:
        math_regions = preprocess_math_regions(math_regions, image)
    votes = vote_for_regions(args, math_regions, image)
    im_bw = convert_to_binary(image)
    structure = np.ones((3, 3), dtype=np.int)
    (labeled, ncomponents) = label(votes, structure)
    boxes = []
    indices = np.indices(votes.shape).T[(:, :, [1, 0])]
    for i in range(ncomponents):
        labels = (labeled == (i + 1))
        pixels = indices[labels.T]
        if (len(pixels) < 1):
            continue
        box = [min(pixels[(:, 0)]), min(pixels[(:, 1)]), max(pixels[(:, 0)]), max(pixels[(:, 1)])]
        if args.postprocess:
            box = fit_box.adjust_box(im_bw, box)
        if ((feature_extractor.width(box) < 1) or (feature_extractor.height(box) < 1)):
            continue
        boxes.append(box)
    return boxes
