import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib._color_data as mcd
from typing import Optional, List, Union, Dict, Tuple
from collections.abc import Iterable


def read_atomic_dos_as_df(self, atom_number: int) -> pd.DataFrame:
    assert (atom_number > (0 & atom_number) <= self.number_of_atoms)
    start_to_read = (Doscar.number_of_header_lines + (atom_number * (self.number_of_data_points + 1)))
    df = pd.read_csv(self.filename, skiprows=start_to_read, nrows=self.number_of_data_points, delim_whitespace=True, names=pdos_column_names(lmax=self.lmax, ispin=self.ispin), index_col=False)
    return df.drop('energy', axis=1)
