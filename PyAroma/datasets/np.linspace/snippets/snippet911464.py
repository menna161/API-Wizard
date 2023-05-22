from __future__ import annotations
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from pymatgen.core import Structure
from typing import List, Optional, Type
from numpy.typing import ArrayLike
from vasppy.utils import dr_ij


def __init__(self, structures: List[Structure], indices: List[int], d_steps: int, nbins: int=500, r_min: float=0.0, r_max: float=10.0):
    '\n        Initialise a VanHoveCorrelationFunction instance.\n\n        Args:\n            structures (list(pymatgen.Structure)): List of pymatgen Structure objects.\n            indices (list(int)): List of indices for species to consider.\n            d_steps (int): number of steps between structures at dt=0 and dt=t.\n            nbins (:obj:`int`, optional): Number of bins used for the RDF. Optional, default is 500.\n            rmin (:obj:`float`, optional): Minimum r value. Optional, default is 0.0.\n            rmax (:obj:`float`, optional): Maximum r value. Optional, default is 10.0.\n\n        Returns:\n             None\n\n        '
    self.nbins = nbins
    self.range = (r_min, r_max)
    self.intervals = np.linspace(r_min, r_max, (nbins + 1))
    self.dr = ((r_max - r_min) / nbins)
    self.r = (self.intervals[:(- 1)] + (self.dr / 2.0))
    self.gdrt = np.zeros(nbins, dtype=np.double)
    self.gsrt = np.zeros(nbins, dtype=np.double)
    rho = (len(indices) / structures[0].lattice.volume)
    lattice = structures[0].lattice
    ff = shell_volumes(self.intervals)
    rho = (len(indices) / lattice.volume)
    for (struc_i, struc_j) in zip(structures[:(len(structures) - d_steps)], structures[d_steps:]):
        i_frac_coords = struc_i.frac_coords[indices]
        j_frac_coords = struc_j.frac_coords[indices]
        dr_ij = lattice.get_all_distances(i_frac_coords, j_frac_coords)
        mask = np.ones(dr_ij.shape, dtype=bool)
        np.fill_diagonal(mask, 0)
        distinct_dr_ij = np.ndarray.flatten(dr_ij[mask])
        hist = np.histogram(distinct_dr_ij, bins=nbins, range=(0.0, r_max), density=False)[0]
        self.gdrt += (hist / rho)
        self_dr_ij = np.ndarray.flatten(dr_ij[np.invert(mask)])
        hist = np.histogram(self_dr_ij, bins=nbins, range=(0.0, r_max), density=False)[0]
        self.gsrt += (hist / rho)
    self.gdrt = (((self.gdrt / ff) / (len(structures) - d_steps)) / float(len(indices)))
    self.gsrt = ((self.gsrt / (len(structures) - d_steps)) / float(len(indices)))
