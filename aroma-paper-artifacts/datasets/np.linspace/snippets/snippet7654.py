from joblib import Parallel, delayed
import h5py
import numpy as np
from numpy.lib.recfunctions import append_fields
import dask.array as da
from dask.diagnostics import ProgressBar
import os
from .generate import generate_events, get_generator_input
from .preprocessing import preprocess, pixel_edges
from .extern.six import string_types
from .utils import default_inv_roc_curve, lklhd_inv_roc_curve, lklhd_inv_roc_curve2d


def get_flat_weights(pt, pt_min, pt_max, pt_bins):
    (pt_hist, edges) = np.histogram(pt, bins=np.linspace(pt_min, pt_max, (pt_bins + 1)))
    pt_hist = np.true_divide(pt_hist, pt_hist.sum())
    image_weights = np.true_divide(1.0, np.take(pt_hist, (np.searchsorted(edges, pt) - 1)))
    image_weights = np.true_divide(image_weights, image_weights.mean())
    return image_weights
