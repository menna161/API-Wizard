from __future__ import annotations
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from pymatgen.core import Structure
from typing import List, Optional, Type
from numpy.typing import ArrayLike
from vasppy.utils import dr_ij


def __init__(self, structures: List[Structure], indices_i: List[int], indices_j: Optional[List[int]]=None, nbins: int=500, r_min: float=0.0, r_max: float=10.0, weights: Optional[List[float]]=None) -> None:
    '\n        Initialise a RadialDistributionFunction instance.\n\n        Args:\n            structures (list(pymatgen.Structure)): List of pymatgen Structure objects.\n            indices_i (list(int)): List of indices for species i.\n            indices_j (:obj:`list(int)`, optional): List of indices for species j. Optional,\n                default is `None`.\n            nbins (:obj:`int`, optional): Number of bins used for the RDF. Optional, default is 500.\n            rmin (:obj:`float`, optional): Minimum r value. Optional, default is 0.0.\n            rmax (:obj:`float`, optional): Maximum r value. Optional, default is 10.0.\n            weights (:obj:`list(float)`, optional): List of weights for each structure.\n                Optional, default is `None`.\n\n        Returns:\n             None\n\n        '
    if weights:
        if (len(weights) != len(structures)):
            raise ValueError('List of structure weights needs to be the same length as the list of structures.')
    else:
        weights = ([1.0] * len(structures))
    self.self_reference = ((not indices_j) or (indices_j == indices_i))
    if (not indices_j):
        indices_j = indices_i
    self.indices_i = indices_i
    self.indices_j = indices_j
    self.nbins = nbins
    self.range = (r_min, r_max)
    self.intervals = np.linspace(r_min, r_max, (nbins + 1))
    self.dr = ((r_max - r_min) / nbins)
    self.r = (self.intervals[:(- 1)] + (self.dr / 2.0))
    ff = shell_volumes(self.intervals)
    self.coordination_number = np.zeros(nbins)
    self.rdf = np.zeros(nbins, dtype=np.double)
    for (structure, weight) in zip(structures, weights):
        all_dr_ij = dr_ij(structure=structure, indices_i=self.indices_i, indices_j=self.indices_j, self_reference=False).flatten()
        hist = np.histogram(all_dr_ij, bins=nbins, range=(r_min, r_max), density=False)[0]
        rho = (float(len(self.indices_i)) / structure.lattice.volume)
        self.rdf += ((hist * weight) / rho)
        self.coordination_number += np.cumsum(hist)
    self.rdf = (((self.rdf / ff) / sum(weights)) / float(len(indices_j)))
    self.coordination_number = ((self.coordination_number / sum(weights)) / float(len(self.indices_j)))
