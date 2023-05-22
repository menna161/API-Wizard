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


def combine_math_regions(args):
    '\n    It is called for each page in the pdf\n    :param math_files_list:\n    :param image_path:\n    :param output_image:\n    :return:\n    '
    (pdf_name, page_num, math_files_list, char_filepath, image_path, output_image, gt_dir, thresh, output_dir) = args
    try:
        image = cv2.imread(image_path)
        math_regions = read_math_regions((image, pdf_name, page_num, math_files_list))
        char_data = read_char_data(char_filepath)
        math_regions_initial = np.copy(math_regions)
        processed_math_regions = np.copy(math_regions)
        math_regions = voting_algo(math_regions, char_data, image, pdf_name, page_num, output_dir, algorithm=algorithm, thresh_votes=thresh)
        math_regions = np.reshape(math_regions, ((- 1), 4))
        gt_regions = read_gt_regions(gt_dir, pdf_name, page_num)
        if (not os.path.exists(os.path.dirname(output_image))):
            os.mkdir(os.path.dirname(output_image))
        if (if_visualize == 1):
            visualize.draw_all_boxes(image, processed_math_regions, math_regions, gt_regions, output_image)
        col = np.array(([(int(page_num) - 1)] * math_regions.shape[0]))
        math_regions = np.concatenate((col[(:, np.newaxis)], math_regions), axis=1)
        math_file = open(os.path.join(output_dir, (pdf_name + '.csv')), 'a')
        np.savetxt(math_file, math_regions, fmt='%.2f', delimiter=',')
        math_file.close()
    except:
        print('Exception while processing ', pdf_name, ' ', page_num, ' ', sys.exc_info())
    return math_regions
