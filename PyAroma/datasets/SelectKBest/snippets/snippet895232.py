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


@classmethod
def get_breast_cancer(cls):
    print('The copy of UCI ML Breast Cancer Wisconsin (Diagnostic) dataset is downloaded from: https://goo.gl/U2Uwz2')
    print('Internally using load_breast_cancer function from sklearn.datasets ')
    breast_cancer_data = pd.DataFrame(data=load_breast_cancer()['data'], columns=load_breast_cancer()['feature_names'])
    breast_cancer_data['target'] = load_breast_cancer()['target']
    target_dict = dict({j for (i, j) in zip(load_breast_cancer()['target_names'], enumerate(load_breast_cancer()['target_names']))})
    breast_cancer_data['target_names'] = breast_cancer_data['target'].map(target_dict)
    return breast_cancer_data.iloc[(:, :(- 1))]
