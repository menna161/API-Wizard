import warnings
import numpy as np, os, sys, pandas as pd, csv, copy
import torch, torch.nn as nn, matplotlib.pyplot as plt, random
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms
from tqdm import tqdm
import pretrainedmodels.utils as utils
import auxiliaries as aux


def give_VehicleID_datasets(opt):
    '\n    This function generates a training, testing and evaluation dataloader for Metric Learning on the PKU Vehicle dataset.\n    For Metric Learning, training and (multiple) test sets are provided by separate text files, train_list and test_list_<n_classes_2_test>.txt.\n    So no random shuffling of classes.\n\n    Args:\n        opt: argparse.Namespace, contains all traininig-specific parameters.\n    Returns:\n        dict of PyTorch datasets for training, testing and evaluation.\n    '
    train = np.array(pd.read_table((opt.source_path + '/train_test_split/train_list.txt'), header=None, delim_whitespace=True))
    small_test = np.array(pd.read_table((opt.source_path + '/train_test_split/test_list_800.txt'), header=None, delim_whitespace=True))
    medium_test = np.array(pd.read_table((opt.source_path + '/train_test_split/test_list_1600.txt'), header=None, delim_whitespace=True))
    big_test = np.array(pd.read_table((opt.source_path + '/train_test_split/test_list_2400.txt'), header=None, delim_whitespace=True))
    lab_conv = {x: i for (i, x) in enumerate(np.unique(train[(:, 1)]))}
    train[(:, 1)] = np.array([lab_conv[x] for x in train[(:, 1)]])
    lab_conv = {x: i for (i, x) in enumerate(np.unique(np.concatenate([small_test[(:, 1)], medium_test[(:, 1)], big_test[(:, 1)]])))}
    small_test[(:, 1)] = np.array([lab_conv[x] for x in small_test[(:, 1)]])
    medium_test[(:, 1)] = np.array([lab_conv[x] for x in medium_test[(:, 1)]])
    big_test[(:, 1)] = np.array([lab_conv[x] for x in big_test[(:, 1)]])
    train_image_dict = {}
    for (img_path, key) in train:
        if (not (key in train_image_dict.keys())):
            train_image_dict[key] = []
        train_image_dict[key].append((opt.source_path + '/image/{:07d}.jpg'.format(img_path)))
    small_test_dict = {}
    for (img_path, key) in small_test:
        if (not (key in small_test_dict.keys())):
            small_test_dict[key] = []
        small_test_dict[key].append((opt.source_path + '/image/{:07d}.jpg'.format(img_path)))
    medium_test_dict = {}
    for (img_path, key) in medium_test:
        if (not (key in medium_test_dict.keys())):
            medium_test_dict[key] = []
        medium_test_dict[key].append((opt.source_path + '/image/{:07d}.jpg'.format(img_path)))
    big_test_dict = {}
    for (img_path, key) in big_test:
        if (not (key in big_test_dict.keys())):
            big_test_dict[key] = []
        big_test_dict[key].append((opt.source_path + '/image/{:07d}.jpg'.format(img_path)))
    train_dataset = BaseTripletDataset(train_image_dict, opt, samples_per_class=opt.samples_per_class)
    eval_dataset = BaseTripletDataset(train_image_dict, opt, is_validation=True)
    val_small_dataset = BaseTripletDataset(small_test_dict, opt, is_validation=True)
    val_medium_dataset = BaseTripletDataset(medium_test_dict, opt, is_validation=True)
    val_big_dataset = BaseTripletDataset(big_test_dict, opt, is_validation=True)
    return {'training': train_dataset, 'testing_set1': val_small_dataset, 'testing_set2': val_medium_dataset, 'testing_set3': val_big_dataset, 'evaluation': eval_dataset}
