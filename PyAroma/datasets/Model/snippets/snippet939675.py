import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def create_resnet32_cifar_model():
    return ResnetCifar10Model('resnet32_v2', (5, 5, 5))
