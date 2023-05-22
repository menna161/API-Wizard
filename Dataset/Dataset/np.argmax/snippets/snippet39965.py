import numpy as np
import os
from keras.models import load_model
from tqdm import tqdm
import tifffile
import cv2
import glob
from icnet import model_icnet
import argparse
from copy import deepcopy

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument('test_folder', type=str)
    parser.add_argument('output_folder', type=str)
    parser.add_argument('model_file', type=str)
    args = parser.parse_args()
    height = 1024
    width = 1024
    bands = 3
    print(height, width, bands)
    os.environ['CUDA_VISIBLE_DEVICES'] = GPU
    model = model_icnet.build_icnet(height, width, bands, (NUM_CATEGORIES + 1), weights_path=args.model_file, train=False)
    files = glob.glob((args.test_folder + '*LEFT_RGB.tif'))
    nfiles = len(files)
    print('Number of files = ', nfiles)
    for i in tqdm(range(nfiles)):
        name = files[i]
        pos = name.find('LEFT_RGB')
        left_name = name
        name = os.path.basename(name)
        pos = name.find('LEFT_RGB')
        cls_name = ((args.output_folder + name[0:pos]) + 'LEFT_CLS.tif')
        viz_name = ((args.output_folder + name[0:pos]) + 'SEGMENTATION_RGB.tif')
        img = tifffile.imread(left_name)
        img = np.expand_dims(img, axis=0)
        img = ((img - 127.5) / 255.0)
        seg = np.argmax(model.predict(img)[(0, :, :, 0:NUM_CATEGORIES)], axis=2)
        tifffile.imsave(viz_name, category_to_color(seg))
        seg = sequential_to_las_labels(seg)
        tifffile.imsave(cls_name, seg, compress=6)
