import numpy as np
from matplotlib import path


def parse(self, defstring):
    bits = defstring.split(',')
    bits = np.array([float(b) for b in bits])
    assert ((len(bits) % 2) == 0)
    self.n_vertices = (len(bits) / 2)
    self.ra = bits[(np.arange(self.n_vertices) * 2)]
    self.dec = bits[((np.arange(self.n_vertices) * 2) + 1)]
