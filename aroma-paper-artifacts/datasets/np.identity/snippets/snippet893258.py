import numpy as np
from .. import _base


@classmethod
def identity(cls):
    'Return the identity rotation.'
    return cls(np.identity(cls.dim))
