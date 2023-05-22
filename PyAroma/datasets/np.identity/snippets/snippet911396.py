import numpy as np
import sys
import re
import copy
from vasppy import configuration, atom, cell
from vasppy.units import angstrom_to_bohr
from pymatgen.core import Lattice as pmg_Lattice
from pymatgen.core import Structure as pmg_Structure
from pymatgen.io.cif import CifWriter
from collections import Counter
from signal import signal, SIGPIPE, SIG_DFL


def __init__(self):
    self.title = 'Title'
    self.scaling = 1.0
    self.cell = cell.Cell(np.identity(3))
    self.atoms = ['A']
    self.atom_numbers = [1]
    self.coordinate_type = 'Direct'
    self.coordinates = np.array([[0.0, 0.0, 0.0]])
    self.selective_dynamics = False
