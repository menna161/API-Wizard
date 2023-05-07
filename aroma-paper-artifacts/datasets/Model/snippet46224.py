import argparse
import os
import sys
import traceback
import time
import warnings
import pickle
from collections import OrderedDict
import yaml
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import h5py


def load_model(self, model, **model_args):
    Model = import_class(model)
    model = Model(**model_args)
    self.model_text += ('\n\n' + str(model))
    return model
