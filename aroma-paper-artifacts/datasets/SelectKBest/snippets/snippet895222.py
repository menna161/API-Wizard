import numpy as np
from itertools import combinations
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_boston
from tqdm import tqdm
from sklearn.feature_selection import SelectKBest, chi2, f_regression, f_classif
import pandas as pd
from plotly import offline
from plotly.offline import init_notebook_mode, iplot
import cufflinks as cf
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from scipy.misc import factorial
import statsmodels.api as sm
from functools import reduce
import math
import random
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.models.formatters import NumeralTickFormatter


def get_top_k(self):
    columns = list(self.data.columns.values)
    columns.remove(self.target)
    if self.objective:
        top_k_vars = SelectKBest(f_regression, k=self.top_k)
        top_k_vars.fit_transform(self.data[columns], self.data[self.target])
    else:
        columns.remove('intercept')
        try:
            top_k_vars = SelectKBest(chi2, k=self.top_k)
            top_k_vars.fit_transform(self.data[columns], self.data[self.target])
        except:
            top_k_vars = SelectKBest(f_classif, k=self.top_k)
            top_k_vars.fit_transform(self.data[columns], self.data[self.target])
    return [columns[i] for i in top_k_vars.get_support(indices=True)]
