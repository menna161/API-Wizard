from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.offsetbox as offsetbox
import palettable
from collections import defaultdict


def add_continuous_data(self, data, mapping='binary', tick_style='normal', value_range=None, cat_mapping=None, name=None):
    "Add a sample level continuous data to the CoMut object\n\n        Params:\n        -----------\n        data: pandas dataframe\n            A tidy dataframe containing data. Required columns are\n            sample, category, and value. Other columns are ignored.\n            Currently, only one category is allowed.\n\n        mapping: str, colors.LinearSegmentedColormap, default 'binary'\n            A mapping of continuous value to color. Can be defined as\n            matplotlib colormap (str) or a custom LinearSegmentedColormap\n            Samples with missing information are colored according to 'Absent'.\n\n        value_range: tuple or list\n            min and max value of the data. Data will be normalized using\n            this range to fit (0, 1). Defaults to the range of the data.\n\n        cat_mapping: dict\n            Mapping from a discrete category to patch color. Primarily used\n            to override defaults for 'Absent' and 'Not Available' but can\n            be used to mix categorical and continuous values in the same data.\n\n        name: str\n            The name of the dataset being added. Used to references axes.\n            defaults to the integer index of the plot being added.\n\n        tick_style: str, default='normal', 'italic', 'oblique'\n            Tick style to be used for the y axis ticks (category names).\n\n        Returns:\n        --------\n        None"
    req_cols = {'sample', 'category', 'value'}
    if (not req_cols.issubset(data.columns)):
        missing_cols = (req_cols - set(data.columns))
        msg = ', '.join(list(missing_cols))
        raise ValueError('Data missing required columns: {}'.format(msg))
    samples = list(data['sample'].drop_duplicates())
    if (self.samples is None):
        self.samples = samples
    else:
        self._check_samples(samples)
    if (len(set(data['category'])) > 1):
        raise ValueError('Only one category is allowed for continuous data')
    if (name is None):
        name = len(self._plots)
    if (value_range is None):
        data_max = pd.to_numeric(data['value'], 'coerce').max()
        data_min = pd.to_numeric(data['value'], 'coerce').min()
    else:
        (data_min, data_max) = value_range
    if (cat_mapping is None):
        cat_mapping = {'Absent': {'facecolor': 'white'}, 'Not Available': {'facecolor': 'none', 'edgecolor': 'black', 'linewidth': 1}}
    else:
        cat_mapping = cat_mapping.copy()
        if ('Absent' not in cat_mapping):
            cat_mapping['Absent'] = {'facecolor': 'white'}
        if ('Not Available' not in cat_mapping):
            cat_mapping['Not Available'] = {'facecolor': 'none', 'edgecolor': 'black', 'linewidth': 1}
    for (key, value) in cat_mapping.items():
        if (not isinstance(value, dict)):
            mapping[key] = {'facecolor': value}

    def normalize(x):
        if isinstance(x, (int, float)):
            return ((x - data_min) / data_max)
        else:
            return x
    norm_data = data.copy()
    norm_data.loc[(:, 'value')] = data.loc[(:, 'value')].apply(normalize)
    if isinstance(mapping, str):
        mapping = plt.get_cmap(mapping)
    elif (not isinstance(mapping, colors.LinearSegmentedColormap)):
        raise ValueError('Invalid color map for continuous data. Valid types are colormap str or LinearSegmentedColormap')
    dict_mapping = {}
    for value in norm_data.loc[(:, 'value')]:
        if isinstance(value, (int, float)):
            dict_mapping[value] = {'facecolor': mapping(value)}
    dict_mapping.update(cat_mapping)
    category_order = list(norm_data['category'].drop_duplicates())
    parsed_data = self._parse_categorical_data(data=norm_data, category_order=category_order, sample_order=self.samples, value_order=[], priority=[])
    plot_data = {'data': parsed_data, 'patches_options': dict_mapping, 'tick_style': tick_style, 'type': 'continuous', 'range': value_range, 'colorbar': mapping}
    self._plots[name] = plot_data
    return None
