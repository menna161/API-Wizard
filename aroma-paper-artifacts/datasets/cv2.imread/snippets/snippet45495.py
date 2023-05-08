import numpy as np
import cv2
import copy
import os
import sys
from multiprocessing import Pool


def resize_gt(pdf_name='Alford94'):
    image_filelist = [file for file in os.listdir(os.path.join(image_dir, pdf_name)) if file.endswith('.png')]
    math_filepath = os.path.join(math_dir, (pdf_name + '.math'))
    math_file_present = os.path.isfile(math_filepath)
    char_filepath = os.path.join(char_dir, (pdf_name + '.char'))
    char_file_present = os.path.isfile(char_filepath)
    if math_file_present:
        math_file = open(math_filepath, 'r')
        boxes = {}
        for line in math_file:
            box = line.split(',')
            idx = (int(box[0]) + 1)
            box = box[1:]
            box = list(map(int, box))
            if (idx not in boxes):
                boxes[idx] = []
            boxes[idx].append(box)
    if char_file_present:
        char_file = open(char_filepath, 'r')
        char_boxes = {}
        for line in char_file:
            char_box = line.split(',')
            idx = (int(char_box[0]) + 1)
            char_box = char_box[2:]
            if (idx not in char_boxes):
                char_boxes[idx] = []
            char_boxes[idx].append(char_box)
    for image_filepath in image_filelist:
        image = cv2.imread(os.path.join(image_dir, pdf_name, image_filepath))
        basename = os.path.basename(image_filepath)
        page_id = int(os.path.splitext(basename)[0])
        original_width = image.shape[1]
        original_height = image.shape[0]
        resized_image = cv2.imread(os.path.join(resized_image_dir, pdf_name, image_filepath))
        intermediate_width = resized_image.shape[1]
        intermediate_height = resized_image.shape[0]
        intermediate_width_ratio = (intermediate_width / original_width)
        intermediate_height_ratio = (intermediate_height / original_height)
        final_width_ratio = ((final_width * intermediate_width_ratio) / intermediate_width)
        final_height_ratio = ((final_height * intermediate_height_ratio) / intermediate_height)
        final_image = cv2.resize(resized_image, (final_height, final_width))
        if math_file_present:
            if (page_id in boxes):
                current_boxes = boxes[page_id]
            else:
                current_boxes = []
            for box in current_boxes:
                box[0] = int(np.round((box[0] * final_width_ratio)))
                box[1] = int(np.round((box[1] * final_height_ratio)))
                box[2] = int(np.round((box[2] * final_width_ratio)))
                box[3] = int(np.round((box[3] * final_height_ratio)))
        if char_file_present:
            if (page_id in char_boxes):
                current_char_boxes = char_boxes[page_id]
            else:
                current_char_boxes = []
            for box in current_char_boxes:
                box[0] = int(np.round((float(box[0]) * final_width_ratio)))
                box[1] = int(np.round((float(box[1]) * final_height_ratio)))
                box[2] = int(np.round((float(box[2]) * final_width_ratio)))
                box[3] = int(np.round((float(box[3]) * final_height_ratio)))
        if (not os.path.exists(os.path.join(output_image_dir, pdf_name))):
            os.makedirs(os.path.join(output_image_dir, pdf_name))
        if (not os.path.exists(os.path.join(output_math_dir, pdf_name))):
            os.makedirs(os.path.join(output_math_dir, pdf_name))
        if (not os.path.exists(os.path.join(output_char_dir, pdf_name))):
            os.makedirs(os.path.join(output_char_dir, pdf_name))
        print('Processing image : ', pdf_name, '/', page_id)
        cv2.imwrite(os.path.join(output_image_dir, pdf_name, (str(page_id) + '.png')), final_image)
        if math_file_present:
            out_math_file = os.path.join(output_math_dir, pdf_name, (str(page_id) + '.pmath'))
            out_math = open(out_math_file, 'w')
            for box in current_boxes:
                out_math.write((','.join((str(x) for x in box)) + '\n'))
            out_math.close()
        if char_file_present:
            out_char_file = os.path.join(output_char_dir, pdf_name, (str(page_id) + '.pchar'))
            out_char = open(out_char_file, 'w')
            for box in current_char_boxes:
                out_char.write((','.join((str(x) for x in box)) + '\n'))
            out_char.close()
