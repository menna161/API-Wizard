import librosa as lr
import nnabla as nn
import nnabla.functions as F
import numpy as np
from librosa.filters import mel as librosa_mel_fn
from nnabla.random import prng
from scipy.ndimage import interpolation
from .misc import RandomSplit


def random_flip(x):
    'Random flipping sign of a Variable.\n\n    Args:\n        x (nn.Variable): Input Variable.\n    '
    shape = (x.shape[0], 1, 1)
    scale = ((2 * F.randint(0, 2, shape=shape)) - 1)
    return (x * scale)
