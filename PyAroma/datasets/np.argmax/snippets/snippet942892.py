import numpy as np
from tadataka.flow_estimation.regularizer import GemanMcClure
from tadataka.utils import is_in_image_range


def step(energy_map):
    return diff_to_neighbors_[np.argmax(energy_map)]
