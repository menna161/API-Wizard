import os
import numpy as np
import hickle as hkl
import glob
from sklearn.model_selection import train_test_split
from PIL import Image
import argparse


def main():
    ' Create image datasets. Processes images and saves them in train,\n    val, test splits. For each split, this creates a numpy array w/\n    dimensions n_images, height, width, depth.\n    '
    parser = argparse.ArgumentParser(description='Process input arguments')
    parser.add_argument('--raw_data', default='./data/UCSD_Anomaly_Dataset.v1p2/', type=str, dest='raw_data', help='data folder mounting point')
    parser.add_argument('--preprocessed_data', default='./data/preprocessed/', type=str, dest='preprocessed_data', help='data folder mounting point')
    parser.add_argument('--n_frames', default=200, type=int, dest='n_frames', help='length of video sequences in input data')
    parser.add_argument('--dataset', dest='dataset', default='UCSDped1', help='the dataset that we are using', type=str, required=False)
    test_size = 0.5
    args = parser.parse_args()
    raw_data = os.path.join(args.raw_data, args.dataset)
    preprocessed_data_path = os.path.join(args.preprocessed_data, args.dataset)
    assert (args.dataset in ['UCSDped1', 'UCSDped2']), ('Dataset (%s) not valid.' % args.dataset)
    if (not (preprocessed_data_path is None)):
        os.makedirs(preprocessed_data_path, exist_ok=True)
        print(('%s created' % preprocessed_data_path))
    desired_im_sz = (152, 232)
    skip_frames = 0
    print('Input data:', raw_data)
    recordings = glob.glob(os.path.join(raw_data, 'Train', 'Train*[0-9]'))
    recordings = sorted(recordings)
    n_recordings = len(recordings)
    print(('Found %s recordings for training' % n_recordings))
    (print('Folders: '),)
    print(os.listdir(os.path.join(raw_data, 'Train')))
    train_recordings = list(zip(([raw_data] * n_recordings), recordings))
    recordings = glob.glob(os.path.join(raw_data, 'Test', 'Test*[0-9]'))
    recordings = sorted(recordings)
    n_recordings = len(recordings)
    print(('Found %s recordings for validation and testing' % n_recordings))
    print(('Using %d percent for testing' % (test_size * 100)))
    (print('Folders: '),)
    print(os.listdir(os.path.join(raw_data, 'Test')))
    recordings = list(zip(([raw_data] * n_recordings), recordings))
    (val_recordings, test_recordings) = train_test_split(recordings, test_size=test_size, random_state=123)
    splits = {s: [] for s in ['train', 'test', 'val']}
    splits['train'] = train_recordings
    splits['val'] = val_recordings
    splits['test'] = test_recordings
    for split in splits:
        im_list = []
        source_list = []
        i = 0
        for (_, folder) in splits[split]:
            files = glob.glob(os.path.join(folder, '*.tif'), recursive=False)
            files = sorted(files)
            for skip in range(0, (skip_frames + 1)):
                for (c, f) in enumerate(files):
                    if ((c % (skip_frames + 1)) == skip):
                        im_list.append(f)
                        source_list.append(os.path.dirname(f))
                        i += 1
        print((((('Creating ' + split) + ' data set with ') + str(len(im_list))) + ' images'))
        X = np.zeros((((len(im_list),) + desired_im_sz) + (3,)), np.uint8)
        for (i, im_file) in enumerate(im_list):
            try:
                im = Image.open(im_file).convert(mode='RGB')
            except Exception as e:
                print(e)
                print(im_file)
                print("something with this file. You can open and investigate manually. It's probably OK to ignore, unless you geta ton of these warnings.")
            try:
                X[i] = np.asarray(process_im(im, desired_im_sz))
            except Exception as e:
                print(e)
                print(im_file)
                raise
        if (split in ['val', 'test']):
            print(('Creating anomaly dataset for %s split' % split))
            anom_anot_filename = os.path.join(raw_data, 'Test', ('%s.m' % args.dataset))
            with open(anom_anot_filename, 'r') as f:
                lines = f.readlines()
            del lines[0]
            anom_indices = []
            for (l, line) in enumerate(lines):
                line = line.replace(':', ',')
                anom_index = line.split('[')[1].split(']')[0].split(',')
                anom_indices.append(anom_index)
            anoms = np.zeros(X.shape[0])
            for (f, folder) in enumerate(splits[split]):
                row = int(os.path.basename(folder[1])[(- 3):])
                anom = anom_indices[(row - 1)]
                while (len(anom) > 0):
                    first_frame = (int(anom.pop(0)) + (row * args.n_frames))
                    last_frame = (int(anom.pop(0)) + (row * args.n_frames))
                    anoms[first_frame:last_frame] = 1
                    hkl.dump(anoms, os.path.join(preprocessed_data_path, (('y_' + split) + '.hkl')))
        hkl.dump(X, os.path.join(preprocessed_data_path, (('X_' + split) + '.hkl')))
        hkl.dump(source_list, os.path.join(preprocessed_data_path, (('sources_' + split) + '.hkl')))
