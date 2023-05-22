import cv2
import os
import argparse
import configparser
import numpy as np
import pandas as pd
from tqdm import tqdm
from natsort import natsorted
import xml.etree.cElementTree as ET
import xml.etree.ElementTree as ET


def vis_one_video(res_file, frame_rate, img_width, img_height, img_dir, output_name):
    try:
        res = np.loadtxt(res_file, delimiter=',')
    except:
        res = np.loadtxt(res_file, delimiter=' ')
    res[(:, 4:6)] += res[(:, 2:4)]
    res = pd.DataFrame(res)
    res = res.replace([np.inf, (- np.inf)], np.nan)
    res = res.dropna()
    res_group = res.groupby(0)
    vid_writer = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*'MJPG'), frame_rate, (img_width, img_height))
    img_names = natsorted(os.listdir(img_dir))
    color_dict = {}
    for (i, img_name) in tqdm(enumerate(img_names), ncols=20):
        img = cv2.imread(os.path.join(img_dir, img_name))
        frame = int(os.path.splitext(img_name)[0])
        if (frame not in res_group.groups.keys()):
            vid_writer.write(img)
            continue
        bboxes = res_group.get_group(frame).values
        for bbox in bboxes:
            if (bbox[1] in color_dict):
                color = color_dict[bbox[1]]
            else:
                color = np.round((np.random.rand(3) * 255))
                color_dict[bbox[1]] = color
            cv2.rectangle(img, tuple(bbox[4:6].astype(int)), tuple(bbox[2:4].astype(int)), color=color, thickness=3)
            cv2.putText(img, ((str(bbox[6]) + ' ') + str(bbox[7])[0:5]), tuple(bbox[2:4].astype(int)), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
        vid_writer.write(img)
    vid_writer.release()
