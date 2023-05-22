import argparse
import glob
import os
from shutil import copy
import h5py
import soundfile as sf
import numpy as np
import torch
from torch import nn
import tqdm
from fairseq.models.wav2vec import Wav2VecModel


def __init__(self, fname, gpu=0):
    self.gpu = gpu
    self.model = PretrainedWav2VecModel(fname).cuda(gpu)
