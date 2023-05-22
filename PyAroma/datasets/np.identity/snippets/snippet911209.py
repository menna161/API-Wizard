import unittest
from unittest.mock import Mock, patch, mock_open
from io import StringIO
from vasppy.poscar import Poscar
from vasppy.cell import Cell
import numpy as np
from collections import Counter


def setUp(self):
    self.poscar = Poscar()
    self.poscar.title = 'Title'
    self.poscar.scaling = 1.0
    self.poscar.cell = Mock(spec=Cell)
    self.poscar.cell.matrix = np.identity(3)
    self.poscar.atoms = ['A']
    self.poscar.atom_numbers = [1]
    self.poscar.coordinate_type = 'Direct'
    self.poscar.coordinates = np.array([[0.0, 0.0, 0.0]])
    self.poscar.selective_dynamics = False
