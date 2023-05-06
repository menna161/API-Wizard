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
