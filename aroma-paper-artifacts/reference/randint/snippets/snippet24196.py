import os
import matplotlib.pyplot as plt
import nnabla as nn
import nnabla.communicators as C
import nnabla.functions as F
import numpy as np
import seaborn as sns
from nnabla.ext_utils import get_extension_context
from nnabla.function import PythonFunction
from nnabla.initializer import UniformInitializer
from nnabla.parameter import get_parameter_or_create
from nnabla.parametric_functions import parametric_function_api
from sklearn.manifold import TSNE


def _mask_gen(self, b, n):
    (idx_0, idx_1) = ([], [])
    for i in range(b):
        idx = np.cumsum([self.rng.randint(self.lo, self.hi) for _ in range((n // self.lo))])
        idx = idx[(idx < n)]
        partition = np.split(np.arange(n), idx)
        self.rng.shuffle(partition)
        idx_0.append(np.repeat(i, n))
        idx_1.append(np.hstack(partition))
    idx_0 = np.vstack(idx_0)
    idx_1 = np.vstack(idx_1)
    return np.concatenate(([idx_0], [idx_1]))
