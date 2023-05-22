import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def create_resnet152_model():
    return ResnetModel('resnet152', (3, 8, 36, 3))
