import sys
import cv2
import os
import csv
import numpy as np
from multiprocessing import Pool
import shutil


def find_math(args):
    try:
        (pdf_name, image_file, char_file, page_num, output_file) = args
        char_info = {}
        char_map = {}
        image = cv2.imread(image_file)
        with open(char_file) as csvfile:
            char_reader = csv.reader(csvfile, delimiter=',')
            for row in char_reader:
                char_info[row[1]] = row[2:]
                if (row[(- 3)] != 'NONE'):
                    if (row[1] not in char_map):
                        char_map[row[1]] = set()
                    char_map[row[1]].add(row[(- 2)])
                    if (row[(- 2)] not in char_map):
                        char_map[row[(- 2)]] = set()
                    char_map[row[(- 2)]].add(row[1])
                elif (row[(- 4)] == 'MATH_SYMBOL'):
                    if (row[1] not in char_map):
                        char_map[row[1]] = set()
        math_regions_chars = group_math(char_map)
        math_regions = create_bb(math_regions_chars, char_info)
        multi_char_math = set({x for v in math_regions_chars for x in v})
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        writer = csv.writer(open(output_file, 'a'), delimiter=',')
        for math_region in math_regions:
            math_region.insert(0, (int(page_num) - 1))
            writer.writerow(math_region)
        print('Saved ', output_file, ' > ', page_num, ' math ->', len(math_regions))
    except:
        print('Exception while processing ', pdf_name, ' ', page_num, ' ', sys.exc_info())
