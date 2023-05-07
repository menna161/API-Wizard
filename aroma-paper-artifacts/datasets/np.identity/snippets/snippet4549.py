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


def get_multivariate_simple():
    dim = 3
    scale = np.identity(3, dtype=np.float32)
    num_datapoints = 4
    data = np.array([[0.0, 1.0, 0.0], [(- 0.2), 1.1, 0.1], [0.5, 1.2, 0.2], [1.0, (- 0.2), (- 1.2)]], dtype=np.float32)

    def multivariate_normal_model(num_datapoints):
        A = ed.Wishart(df=dim, scale=scale, name='A')
        x = ed.MultivariateNormalFullCovariance(loc=tf.zeros(dim), covariance_matrix=A, name='x')
        loc = (tf.ones([num_datapoints, 1]) * x)
        y = ed.Normal(loc=loc, scale=1.0, name='y')
        return y
    model_args = [num_datapoints]
    observed = {'y': data}
    varnames = ['V', 'x']
    param_names = [p for v in varnames for p in ((v + '_a'), (v + '_b'), (v + '_c'))]
    noncentered_parameterization = {p: 0.0 for p in param_names}
    make_to_centered = build_make_to_centered(multivariate_normal_model, model_args=model_args, observed_data=observed)
    make_to_partially_noncentered = build_make_to_partially_noncentered(multivariate_normal_model, model_args=model_args, observed_data=observed)
    to_centered = make_to_centered(**noncentered_parameterization)
    to_noncentered = make_to_noncentered(multivariate_normal_model, model_args=model_args, observed_data=observed)
    return ModelConfig(multivariate_normal_model, model_args, observed, to_centered, to_noncentered, make_to_centered, make_to_partially_noncentered, None)
