import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def create_resnet56_v2_cifar_model():
    return ResnetCifar10Model('resnet56_v2', (9, 9, 9))
