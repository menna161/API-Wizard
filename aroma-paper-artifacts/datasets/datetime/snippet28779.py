import warnings
import numpy as np, os, sys, pandas as pd, csv, random, datetime
import torch, torch.nn as nn
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle as pkl
from sklearn import metrics
from sklearn import cluster
import faiss
import losses as losses
from scipy.special import comb
from graphviz import Digraph


def set_logging(opt):
    '\n    Generate the folder in which everything is saved.\n    If opt.savename is given, folder will take on said name.\n    If not, a name based on the start time is provided.\n    If the folder already exists, it will by iterated until it can be created without\n    deleting existing data.\n    The current opt.save_path will be extended to account for the new save_folder name.\n\n    Args:\n        opt: argparse.Namespace, contains all training-specific parameters.\n    Returns:\n        Nothing!\n    '
    checkfolder = ((opt.save_path + '/') + opt.savename)
    if (opt.savename == ''):
        date = datetime.datetime.now()
        time_string = '{}-{}-{}-{}-{}-{}'.format(date.year, date.month, date.day, date.hour, date.minute, date.second)
        checkfolder = ((opt.save_path + '/{}_{}_'.format(opt.dataset.upper(), opt.arch.upper())) + time_string)
    counter = 1
    while os.path.exists(checkfolder):
        checkfolder = ((((opt.save_path + '/') + opt.savename) + '_') + str(counter))
        counter += 1
    os.makedirs(checkfolder)
    opt.save_path = checkfolder
    with open((opt.save_path + '/Parameter_Info.txt'), 'w') as f:
        f.write(gimme_save_string(opt))
    pkl.dump(opt, open((opt.save_path + '/hypa.pkl'), 'wb'))
