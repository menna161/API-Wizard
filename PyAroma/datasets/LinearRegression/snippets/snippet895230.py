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


def complete_model_rsquare(self):
    if (self.data_format == 0):
        print(('Selecting %s Best Predictors for the Model' % self.top_k))
        columns = self.get_top_k()
        print('Selected Predictors : ', columns)
        print()
        if (self.objective == 1):
            print(('*' * 20), ' R-Squared of Complete Model : ', ('*' * 20))
            lin_reg = LinearRegression()
            lin_reg.fit(self.data[columns], self.data[self.target])
            r_squared = lin_reg.score(self.data[columns], self.data[self.target])
            print(('R Squared : %s' % r_squared))
            print()
        else:
            print(('*' * 20), ' Pseudo R-Squared of Complete Model : ', ('*' * 20))
            print()
            if (self.pseudo_r2 == 'mcfadden'):
                print(("MacFadden's R-Squared : %s " % self.McFadden_RSquare(columns)))
            elif (pseudo_r2 == 'nagelkerke'):
                print(('Nagelkerke R-Squared : %s ' % self.Nagelkerke_Rsquare(columns)))
            elif (pseudo_r2 == 'cox_and_snell'):
                print(('Cox and Snell R-Squared : %s ' % self.Cox_and_Snell_Rsquare(columns)))
            else:
                print(('Estrella R-Squared : %s ' % self.Estrella(columns)))
            print()
    else:
        if (self.data_format == 2):
            columns = list(self.data.columns.values)
            d = np.sqrt(self.data.values.diagonal())
            corr_array = ((self.data.values.T / d).T / d)
            self.data = pd.DataFrame(data=corr_array, index=columns)
            self.data.columns = columns
            print()
        columns = list(self.data.columns.values)
        columns.remove(self.target)
        corr_all_matrix = self.data.loc[(columns, [self.target])]
        corr_pred_matrix = self.data.loc[(columns, columns)]
        corr_pred_matrix_inverse = pd.DataFrame(np.linalg.pinv(corr_pred_matrix.values), corr_pred_matrix.columns, corr_pred_matrix.index)
        beta = corr_pred_matrix_inverse.dot(corr_all_matrix)
        corr_all_matrix_transpose = corr_all_matrix.transpose()
        r_squared = corr_all_matrix_transpose.dot(beta)
        print(('R Squared : %s' % r_squared.iloc[(0, 0)]))
        print()
