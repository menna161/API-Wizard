import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib._color_data as mcd
from typing import Optional, List, Union, Dict, Tuple
from collections.abc import Iterable


def read_total_dos(self) -> pd.DataFrame:
    start_to_read: int = Doscar.number_of_header_lines
    df: pd.DataFrame = pd.read_csv(self.filename, skiprows=start_to_read, nrows=self.number_of_data_points, delim_whitespace=True, names=['energy', 'up', 'down', 'int_up', 'int_down'], index_col=False)
    self.energy: np.ndarray = df.energy.values
    df.drop('energy', axis=1)
    self.tdos = df
