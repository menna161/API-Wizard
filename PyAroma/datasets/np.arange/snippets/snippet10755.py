from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import pandas as pd


def read(self):
    df = pd.read_csv('../data/model_{}.csv'.format(self.model))
    self.X = df[['C (GPa)', 'dP/dh (N/m)', 'WpWt']].values
    if (self.yname == 'E*'):
        self.y = EtoEstar(df['E (GPa)'].values)[(:, None)]
    elif (self.yname == 'sigma_y'):
        self.y = df['sy (GPa)'].values[(:, None)]
    idx = np.random.choice(np.arange(len(self.X)), self.n, replace=False)
    self.X = self.X[idx]
    self.y = self.y[idx]
