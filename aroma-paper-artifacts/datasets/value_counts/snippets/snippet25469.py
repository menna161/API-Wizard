import json
import math
import random
import itertools
import numpy as np
import pandas as pd
import scipy as sp
import collections
import threading
from scipy.linalg import eigh, cholesky
from scipy.stats import norm
import scipy.interpolate as interpolate
from optparse import OptionParser
import time
import os
from collections import OrderedDict


def generate_data(self):
    self.df = pd.read_csv(self.options.samplefile, nrows=self.options.numsamples, header=0)
    if self.options.prevent_zero:
        self.quant_col_names = [col['field'] for col in self.sample_json['tables']['fact']['fields'] if (col['type'] == 'quantitative')]
        for quant_col_name in self.quant_col_names:
            self.df[quant_col_name] = (self.df[quant_col_name] - self.df[quant_col_name].min())
    self.cat_col_names = [col['field'] for col in self.sample_json['tables']['fact']['fields'] if (col['type'] == 'categorical')]
    for cat_col_name in self.cat_col_names:
        self.df[cat_col_name] = self.df[cat_col_name].astype('category')
    self.derived_cols = [col for col in self.sample_json['tables']['fact']['fields'] if ('deriveFrom' in col)]
    self.derivates = {}
    for derived_col in self.derived_cols:
        kk = self.df.groupby(derived_col['deriveFrom'])[derived_col['field']].first().to_dict()
        self.derivates[derived_col['field']] = kk
    self.orgdf = self.df.copy()
    self.cat_cols = list(self.orgdf.select_dtypes(include=['category']).columns)
    self.cat_hists = {}
    self.cat_hists_keys = {}
    self.cat_hists_values = {}
    for cat_col in self.cat_cols:
        self.cat_hists[cat_col] = self.df[cat_col].value_counts(normalize=True).to_dict()
        self.cat_hists[cat_col] = OrderedDict(sorted(self.cat_hists[cat_col].items(), key=(lambda x: x[0])))
        self.cat_hists_keys[cat_col] = list(self.cat_hists[cat_col].keys())
        self.cat_hists_values[cat_col] = list(self.cat_hists[cat_col].values())
        del self.df[cat_col]
    self.means = self.df.mean()
    self.stdevs = self.df.std()
    np.set_printoptions(suppress=True)
    for (idx, col) in enumerate(self.df.columns):
        self.df[col] = ((self.df[col] - self.means[col]) / self.stdevs[col])
    self.inv_cdfs = self.get_inverse_cdfs(self.orgdf, self.df)
    covariance = self.df.cov()
    self.decomposition = cholesky(covariance, lower=True)
    num_batches = int(math.ceil((self.options.size / self.options.batchsize)))
    st = current_milli_time()
    for batch_i in range(num_batches):
        print((' %i/%i batches processed.' % (batch_i, num_batches)))
        self.process_batch(batch_i)
    print('done.')
    print((current_milli_time() - st))
