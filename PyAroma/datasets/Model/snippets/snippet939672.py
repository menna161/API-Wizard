import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def create_resnet152_v2_model():
    return ResnetModel('resnet152_v2', (3, 8, 36, 3))
