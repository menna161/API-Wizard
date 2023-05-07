import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def create_resnet44_cifar_model():
    return ResnetCifar10Model('resnet44', (7, 7, 7))
