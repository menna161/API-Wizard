import re
import os
import numpy as np
from utils.io import read_serialized, mkdir
from utils.constants import CONTENT_FOLDER


def random_shape_net(cat_id, is_train):
    cat_id = int(cat_id)
    if is_train:
        assert ((cat_id % 5) != 0)
        shape_id = np.random.choice([x for x in range(SHAPE_NET_NUMS['{:04d}'.format(cat_id)]) if ((x % 5) != 0)])
    elif ((cat_id % 5) == 0):
        shape_id = np.random.randint(0, SHAPE_NET_NUMS['{:04d}'.format(cat_id)])
    else:
        shape_id = np.random.choice([x for x in range(SHAPE_NET_NUMS['{:04d}'.format(cat_id)]) if ((x % 5) == 0)])
    return '{:04d}{:06d}'.format(cat_id, shape_id)
