import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def create_resnet20_cifar_model():
    return ResnetCifar10Model('resnet20', (3, 3, 3))
