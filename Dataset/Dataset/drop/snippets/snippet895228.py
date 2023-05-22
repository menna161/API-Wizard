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


def dominance_level(self):
    gen_dom = self.predict_general_dominance()
    condition_dom = self.predict_conditional_dominance()
    comp_dom = self.predict_complete_dominance()
    gen_dom.rename(columns={'Dominating': 'Generally Dominating'}, inplace=True)
    condition_dom.drop('Conditional Dominance', inplace=True, axis=1)
    condition_dom.rename(columns={'Dominating': 'Conditionally Dominating'}, inplace=True)
    comp_dom.rename(columns={'Dominating': 'Completelly Dominating'}, inplace=True)
    return pd.merge(pd.merge(left=gen_dom, right=condition_dom[['Predictors', 'Conditionally Dominating']], how='left'), comp_dom, how='left').fillna('')
