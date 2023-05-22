import numpy as np
from utils.geometry import deg2rad


def convert_rot_patterns(rot_segments):
    'Convert rotation patterns from lists of start-end-steps to one single array'
    return np.concatenate(list((np.linspace(start=deg2rad(start), stop=deg2rad(stop), num=num) for (start, stop, num) in rot_segments)))
