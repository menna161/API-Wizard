import numpy as np
from utils.geometry import deg2rad


def convert_trans_patterns(trans_segments):
    'Convert translation patterns from lists of start-end-steps to one single array'
    return np.concatenate(list((np.linspace(start=start, stop=stop, num=num) for (start, stop, num) in trans_segments)))
