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


def model_stats(self):
    columns = self.get_top_k()
    model_combinations = self.model_features_combination(columns)
    model_rsquares = {}
    if (self.objective == 1):
        for i in tqdm(model_combinations):
            for j in i:
                train_features = list(j)
                lin_reg = LinearRegression()
                lin_reg.fit(self.data[train_features], self.data[self.target])
                r_squared = lin_reg.score(self.data[list(j)], self.data[self.target])
                model_rsquares[' '.join(train_features)] = r_squared
    else:
        for i in tqdm(model_combinations):
            for j in i:
                train_features = list(j)
                if (self.pseudo_r2 == 'mcfadden'):
                    r_squared = self.McFadden_RSquare(train_features)
                elif (self.pseudo_r2 == 'nagelkerke'):
                    r_squared = self.Nagelkerke_Rsquare(train_features)
                elif (self.pseudo_r2 == 'cox_and_snell'):
                    r_squared = self.Cox_and_Snell_Rsquare(train_features)
                elif (self.pseudo_r2 == 'estrella'):
                    r_squared = self.Estrella(train_features)
                model_rsquares[' '.join(train_features)] = r_squared
    self.model_rsquares = model_rsquares
    return self.model_rsquares
