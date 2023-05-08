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


def read_page_info(filename, annotations_dir, image_dir, gt_dir, char_gt):
    pages_list = []
    pdf_names = open(filename, 'r')
    annotations_map = {}
    char_annotations_map = {}
    for pdf_name in pdf_names:
        pdf_name = pdf_name.strip()
        if (pdf_name != ''):
            if (pdf_name not in annotations_map):
                annotations_map[pdf_name] = {}
            for (root, dirs, _) in os.walk(os.path.join(annotations_dir, pdf_name), topdown=False):
                for dir in dirs:
                    for filename in os.listdir(os.path.join(annotations_dir, pdf_name, dir)):
                        if (filename.endswith('.csv') or filename.endswith('.pmath')):
                            patch_num = os.path.splitext(filename)[0]
                            page_num = os.path.basename(os.path.join(annotations_dir, pdf_name, dir))
                            if (page_num not in annotations_map[pdf_name]):
                                annotations_map[pdf_name][page_num] = []
                            annotations_map[pdf_name][page_num].append(os.path.join(annotations_dir, pdf_name, dir, filename))
            if (pdf_name not in char_annotations_map):
                char_annotations_map[pdf_name] = {}
            for filename in os.listdir(os.path.join(char_gt, pdf_name)):
                if (filename.endswith('.csv') or filename.endswith('.pchar')):
                    page_num = os.path.splitext(filename)[0]
                    char_annotations_map[pdf_name][page_num] = os.path.join(char_gt, pdf_name, filename)
            for (root, dirs, files) in os.walk(os.path.join(char_gt, pdf_name)):
                for name in files:
                    if name.endswith('.pchar'):
                        page_num = os.path.splitext(name)[0]
                        if (page_num in annotations_map[pdf_name]):
                            image = cv2.imread(os.path.join(image_dir, pdf_name, (page_num + '.png')))
                            pages_list.append((image, pdf_name, page_num, annotations_map[pdf_name][page_num]))
    pdf_names.close()
    return (pages_list, annotations_map, char_annotations_map)
