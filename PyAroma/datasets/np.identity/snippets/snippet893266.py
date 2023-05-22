import numpy as np
from .. import _base


@classmethod
def identity(cls):
    'Return the identity transformation.'
    return cls.from_matrix(np.identity(cls.dim))
