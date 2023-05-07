from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import contextlib
import csv
import os
import numpy as np
import pandas as pd
import tensorflow.compat.v1 as tf
from tensorflow_probability import bijectors as tfb
from tensorflow_probability import distributions as tfd
from tensorflow_probability import edward2 as ed
from tensorflow_probability.python.math import psd_kernels
import program_transformations as ed_transforms
import data.electric as electric
import data.election88 as election88
import data.police as police


def load_radon_data(state_code):
    'Load the radon dataset.\n\n  Code from http://mc-stan.org/users/documentation/case-studies/radon.html.\n  (Apache2 licensed)\n  '
    with open_data_file('srrs2.dat') as f:
        srrs2 = pd.read_csv(f)
    srrs2.columns = srrs2.columns.map(str.strip)
    srrs_mn = srrs2.assign(fips=((srrs2.stfips * 1000) + srrs2.cntyfips))[(srrs2.state == state_code)]
    with open_data_file('cty.dat') as f:
        cty = pd.read_csv(f)
    cty_mn = cty[(cty.st == state_code)].copy()
    cty_mn['fips'] = ((1000 * cty_mn.stfips) + cty_mn.ctfips)
    srrs_mn.county = srrs_mn.county.str.strip()
    counties = srrs_mn[['county', 'fips']].drop_duplicates()
    county_map_uranium = {a: b for (a, b) in zip(counties['county'], range(len(counties['county'])))}
    uranium_levels = cty_mn.merge(counties, on='fips')['Uppm']
    srrs_mn_new = srrs_mn.merge(cty_mn[['fips', 'Uppm']], on='fips')
    srrs_mn_new = srrs_mn_new.drop_duplicates(subset='idnum')
    srrs_mn_new.county = srrs_mn_new.county.str.strip()
    mn_counties = srrs_mn_new.county.unique()
    county_lookup = dict(zip(mn_counties, range(len(mn_counties))))
    county = srrs_mn_new['county_code'] = srrs_mn_new.county.replace(county_lookup).values
    radon = srrs_mn_new.activity
    srrs_mn_new['log_radon'] = log_radon = np.log((radon + 0.1)).values
    floor_measure = srrs_mn_new.floor.values
    n_county = srrs_mn_new.groupby('county')['idnum'].count()
    uranium = np.zeros(len(n_county), dtype=np.float32)
    for (k, _) in county_lookup.items():
        uranium[county_lookup[k]] = uranium_levels[county_map_uranium[k]]
    uranium = [(np.log(ur) if (ur > 0.0) else 0.0) for ur in uranium]
    c = county
    u = np.float32(uranium)
    x = np.float32(floor_measure)
    data = np.float32(log_radon).reshape((- 1), 1)
    return (c, u, x, data)
