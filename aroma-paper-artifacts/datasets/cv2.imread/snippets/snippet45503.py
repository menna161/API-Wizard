import sys
import os
from multiprocessing import Pool
import csv
import cv2


def split(args):
    (gt_dir, pdf_name, out_dir, ext) = args
    file_path = os.path.join(gt_dir, ((pdf_name + '.') + ext))
    img_dir = '/home/psm2208/data/GTDB/images/'
    map = {}
    if (ext == 'math'):
        file_ip = open(file_path, 'r')
        for line in file_ip:
            entries = line.strip().split(',')
            if (entries[0] not in map):
                map[entries[0]] = []
            map[entries[0]].append(entries[1:])
        for key in map:
            boxes = map[key]
            key = float(key)
            img_file = os.path.join(img_dir, pdf_name, (str((int(key) + 1)) + '.png'))
            img = cv2.imread(img_file)
            (height, width, channels) = img.shape
            width_ratio = 1
            height_ratio = 1
            file_op = open(((os.path.join(out_dir, pdf_name, str((int(key) + 1))) + '.p') + ext), 'w')
            for box in boxes:
                box[0] = (float(box[0]) * width_ratio)
                box[1] = (float(box[1]) * height_ratio)
                box[2] = (float(box[2]) * width_ratio)
                box[3] = (float(box[3]) * height_ratio)
                file_op.write((','.join((str(e) for e in box)) + '\n'))
            file_op.close()
            file_ip.close()
    elif (ext == 'char'):
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if (row[0] not in map):
                    map[row[0]] = []
                map[row[0]].append(row)
        for key in map:
            boxes = map[key]
            with open(((os.path.join(out_dir, pdf_name, str((int(key) + 1))) + '.p') + ext), 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for box in boxes:
                    writer.writerow(box)
