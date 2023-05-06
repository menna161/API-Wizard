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


def get_german_credit_gammascale():
    'German credit model with Gamma priors on the coefficient scales.'
    (numericals, categoricals, status) = load_german_credit_data()

    def german_credit_model():
        x_numeric = tf.constant(numericals.astype(np.float32))
        x_categorical = [tf.one_hot(c, (c.max() + 1)) for c in categoricals]
        all_x = tf.concat(([x_numeric] + x_categorical), 1)
        num_features = int(all_x.shape[1])
        overall_log_scale = ed.Normal(loc=0.0, scale=10.0, name='overall_log_scale')
        beta_log_scales = ed.TransformedDistribution(tfd.Gamma((0.5 * tf.ones([num_features])), 0.5), bijector=tfb.Invert(tfb.Exp()), name='beta_log_scales')
        beta = ed.Normal(loc=tf.zeros([num_features]), scale=tf.exp((overall_log_scale + beta_log_scales)), name='beta')
        logits = tf.einsum('nd,md->mn', all_x, beta[(tf.newaxis, :)])
        return ed.Bernoulli(logits=logits, name='y')
    observed = {'y': status[(np.newaxis, Ellipsis)]}
    model_args = []
    varnames = ['overall_log_scale', 'beta_log_scales', 'beta']
    param_names = [p for v in varnames for p in ((v + '_a'), (v + '_b'), (v + '_c'))]
    noncentered_parameterization = {p: 0.0 for p in param_names}
    make_to_centered = build_make_to_centered(german_credit_model, model_args=model_args, observed_data=observed)
    make_to_partially_noncentered = build_make_to_partially_noncentered(german_credit_model, model_args=model_args, observed_data=observed)
    to_centered = make_to_centered(**noncentered_parameterization)
    to_noncentered = make_to_noncentered(german_credit_model, model_args=model_args, observed_data=observed)
    return ModelConfig(german_credit_model, model_args, observed, to_centered, to_noncentered, make_to_centered, make_to_partially_noncentered, None)
