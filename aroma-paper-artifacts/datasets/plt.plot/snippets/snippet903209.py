from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.offsetbox as offsetbox
import palettable
from collections import defaultdict


def add_sample_indicators(self, data, name=None, plot_kwargs=None):
    "Add a line plot that indicates samples that share a characteristic\n\n        Params:\n        -----------\n        data: pandas dataframe\n            A tidy dataframe that assigns individual samples to groups.\n            Required columns are 'sample' and 'group'. Other columns are\n            ignored.\n\n        name: str\n            The name of the dataset being added. Used to references axes\n            Defaults to the integer index of the plot being added.\n\n        plot_kwargs: dict\n            dict of kwargs to be passed to plt.plot during plotting. Defaults\n            to {'color': 'black', 'marker': 'o', markersize': 3}\n\n        Returns:\n        --------\n        None"
    req_cols = {'sample', 'group'}
    if (not req_cols.issubset(data.columns)):
        missing_cols = (req_cols - set(data.columns))
        msg = ', '.join(list(missing_cols))
        raise ValueError('Data missing required columns: {}'.format(msg))
    if (name is None):
        name = len(self._plots)
    if (plot_kwargs is None):
        plot_kwargs = {'color': 'black', 'marker': 'o', 'markersize': 3}
    data_indexed = data.set_index('sample', drop=True)
    samples = list(data_indexed.index)
    if (self.samples is None):
        self.samples = samples
    else:
        self._check_samples(samples)
        missing_samples = list((set(self.samples) - set(samples)))
        data_indexed = data_indexed.reindex(self.samples)
    seen_groups = set()
    prev_group = None
    for assignment in data_indexed['group']:
        if ((assignment in seen_groups) and (not np.isnan(assignment))):
            raise ValueError('Samples that share a group must be adjacent in CoMut sample ordering.')
        elif (assignment != prev_group):
            seen_groups.add(prev_group)
            prev_group = assignment
    plot_data = {'data': data_indexed, 'plot_options': plot_kwargs, 'type': 'indicator'}
    self._plots[name] = plot_data
    return None
