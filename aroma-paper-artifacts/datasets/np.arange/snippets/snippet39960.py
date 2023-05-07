from os.path import join
from pathlib import Path
from sys import stderr
import numpy as np
import os
from copy import deepcopy
from tqdm import tqdm
import tifffile
import glob


def convert_files_to_npz(input_folder, out_folder, out_prefix):
    files = glob.glob((input_folder + '*LEFT_RGB*.tif'))
    num = len(files)
    print('Number of images = ', num)
    if (num == 0):
        print('No matching files found', file=stderr)
        return
    train_fraction = TRAIN_FRACTION
    num_train = int((train_fraction * num))
    max_per_train = MAX_IMAGES_PER_TRAIN_FILE
    print('Number of training images = ', num_train)
    print('Number of validation images = ', (num - num_train))
    count = 0
    num_files = 0
    disparities = []
    lefts = []
    rights = []
    left_categories = []
    left_agls = []
    indices = np.arange(num)
    np.random.seed(0)
    np.random.shuffle(indices)
    files = [files[i] for i in indices]
    for i in tqdm(range(num)):
        left_name = os.path.basename(files[i])
        start = left_name.find('LEFT_RGB')
        right_name = ((input_folder + left_name[0:start]) + 'RIGHT_RGB.tif')
        left_agl_name = ((input_folder + left_name[0:start]) + 'LEFT_AGL.tif')
        disparity_name = ((input_folder + left_name[0:start]) + 'LEFT_DSP.tif')
        left_cls_name = ((input_folder + left_name[0:start]) + 'LEFT_CLS.tif')
        left_name = (input_folder + left_name)
        left = np.array(tifffile.imread(left_name))
        right = np.array(tifffile.imread(right_name))
        left_cls = np.array(tifffile.imread(left_cls_name))
        disparity = np.array(tifffile.imread(disparity_name))
        left_agl = np.array(tifffile.imread(left_agl_name))
        left_labels = las_to_sequential_labels(left_cls)
        lefts.append(left)
        rights.append(right)
        disparities.append(disparity)
        left_categories.append(left_labels)
        left_agls.append(left_agl)
        count = (count + 1)
        if (((count >= max_per_train) and (i < num_train)) or (i == (num_train - 1))):
            num_files = (num_files + 1)
            print(' ')
            print('Counts for train file ', num_files)
            cats = np.asarray(left_categories)
            max_category = cats.max()
            for j in range(max_category):
                print(j, ': ', len(cats[(cats == j)]))
            print('Writing files...')
            print(' ')
            out_path = Path(out_folder)
            if (not out_path.exists()):
                out_path.mkdir()
            disparity_name = join(out_path, (((out_prefix + '.train.disparity.') + '{:1d}'.format(num_files)) + '.npz'))
            left_name = join(out_path, (((out_prefix + '.train.left.') + '{:1d}'.format(num_files)) + '.npz'))
            right_name = join(out_path, (((out_prefix + '.train.right.') + '{:1d}'.format(num_files)) + '.npz'))
            left_cat_name = join(out_path, (((out_prefix + '.train.left_label.') + '{:1d}'.format(num_files)) + '.npz'))
            left_agl_name = join(out_path, (((out_prefix + '.train.left_agl.') + '{:1d}'.format(num_files)) + '.npz'))
            np.savez_compressed(disparity_name, disparities)
            np.savez_compressed(left_name, lefts)
            np.savez_compressed(right_name, rights)
            np.savez_compressed(left_cat_name, left_categories)
            np.savez_compressed(left_agl_name, left_agls)
            count = 0
            disparities = []
            lefts = []
            rights = []
            left_categories = []
            left_agls = []
    print(' ')
    print('Counts for validation file')
    cats = np.asarray(left_categories)
    max_category = cats.max()
    for j in range(max_category):
        print(j, ': ', len(cats[(cats == j)]))
    print('Writing files...')
    print(' ')
    out_path = Path(out_folder)
    if (not out_path.exists()):
        out_path.mkdir()
    print('Writing validation files')
    print('Number of validation samples = ', len(disparities))
    disparity_name = join(out_path, (out_prefix + '.test.disparity.npz'))
    left_name = join(out_path, (out_prefix + '.test.left.npz'))
    right_name = join(out_path, (out_prefix + '.test.right.npz'))
    left_cat_name = join(out_path, (out_prefix + '.test.left_label.npz'))
    left_agl_name = join(out_path, (out_prefix + '.test.left_agl.npz'))
    np.savez_compressed(disparity_name, disparities)
    np.savez_compressed(left_name, lefts)
    np.savez_compressed(right_name, rights)
    np.savez_compressed(left_cat_name, left_categories)
    np.savez_compressed(left_agl_name, left_agls)
