import os
import tempfile
from unittest import TestCase
import torch
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_adabound import AdaBound
from adabound import AdaBound as OfficialAdaBound


@staticmethod
def gen_torch_linear(w, b):
    linear = torch.nn.Linear(3, 5)
    linear.weight = torch.nn.Parameter(torch.Tensor(w.transpose().tolist()))
    linear.bias = torch.nn.Parameter(torch.Tensor(b.tolist()))
    return linear
