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
from sklearn.cluster import AgglomerativeClustering


def fusion_stitch_grid(filename, annotations_dir, output_dir, image_dir='/home/psm2208/data/GTDB/images/', gt_dir='/home/psm2208/data/GTDB/', char_gt='', thresh=20):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    if (not os.path.exists(output_dir)):
        os.mkdir(output_dir)
    pages_list = read_page_info(filename, annotations_dir, image_dir, gt_dir, char_gt)
    pool = Pool(processes=32)
    total = str(len(pages_list))
    math_cache = pool.map(read_math_regions, pages_list)
    pool.close()
    pool.join()
    fusion_list = []
    for (i, page) in enumerate(pages_list):
        pdf_name = page[1]
        page_num = page[2]
        for a in np.arange(0.3, 1.1, 0.1):
            for b in np.arange(0.0, 1.1, 0.1):
                for c in np.arange(0.0, 1.1, 0.1):
                    fusion_list.append((pdf_name, page_num, output_dir, math_cache[i], a, b, c))
    pool = Pool(processes=32)
    total = str(len(fusion_list))
    start = time.time()
    init = start
    for (i, _) in enumerate(pool.imap_unordered(fusion, fusion_list), 1):
        print(((('\nprogress: ' + str(i)) + '/') + total))
        if ((i % 100) == 0):
            current = time.time()
            print('\nTime taken for last 100, total time:', (current - start), (current - init))
            start = time.time()
    pool.close()
    pool.join()
