import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def create_resnet110_cifar_model():
    return ResnetCifar10Model('resnet110', (18, 18, 18))
