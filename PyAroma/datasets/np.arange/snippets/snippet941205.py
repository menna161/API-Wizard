from IPython import embed
import argparse
import itertools
from operator import itemgetter
import os
import re
import time
from PIL import Image
from tensorboardX import SummaryWriter
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import datasets, transforms, utils
import tqdm
import wandb
from baseline import PixelCNN
from layers import PONO
from masking import *
from model import OurPixelCNN
from utils import *
from apex import amp
from celeba_data import get_celeba_dataloader


def random_resized_obs():
    idx = np.arange(len(resized_obses))
    obs_i = np.random.choice(idx, p=args.resize_probs)
    return resized_obses[int(obs_i)]
