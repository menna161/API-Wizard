import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def create_resnet50_model():
    return ResnetModel('resnet50', (3, 4, 6, 3))
