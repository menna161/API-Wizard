import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def create_resnet50_v2_model():
    return ResnetModel('resnet50_v2', (3, 4, 6, 3))
