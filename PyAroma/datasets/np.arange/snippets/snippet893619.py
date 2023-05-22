import logging
import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import DataLoader
from tqdm import trange
from pyodds.algo.algorithm_utils import deepBase, PyTorchUtils
from pyodds.algo.autoencoder import AutoEncoderModule
from pyodds.algo.lstmencdec import LSTMEDModule
from pyodds.algo.base import Base


def decision_function(self, X: pd.DataFrame):
    'Predict raw anomaly score of X using the fitted detector.\n        The anomaly score of an input sample is computed based on different\n        detector algorithms. For consistency, outliers are assigned with\n        larger anomaly scores.\n        Using the learned mixture probability, mean and covariance for each component k, compute the energy on the\n        given data.\n\n        Parameters\n        ----------\n        X : dataframe of shape (n_samples, n_features)\n            The training input samples. Sparse matrices are accepted only\n            if they are supported by the base estimator.\n        Returns\n        -------\n        anomaly_scores : numpy array of shape (n_samples,)\n            The anomaly score of the input samples.\n        '
    self.dagmm.eval()
    X.interpolate(inplace=True)
    X.bfill(inplace=True)
    data = X.values
    sequences = [data[i:(i + self.sequence_length)] for i in range(((len(data) - self.sequence_length) + 1))]
    data_loader = DataLoader(dataset=sequences, batch_size=1, shuffle=False)
    test_energy = np.full((self.sequence_length, X.shape[0]), np.nan)
    encodings = np.full((self.sequence_length, X.shape[0], self.hidden_size), np.nan)
    decodings = np.full((self.sequence_length, X.shape[0], X.shape[1]), np.nan)
    euc_errors = np.full((self.sequence_length, X.shape[0]), np.nan)
    csn_errors = np.full((self.sequence_length, X.shape[0]), np.nan)
    for (i, sequence) in enumerate(data_loader):
        (enc, dec, z, _) = self.dagmm(self.to_var(sequence).float())
        (sample_energy, _) = self.dagmm.compute_energy(z, size_average=False)
        idx = ((i % self.sequence_length), np.arange(i, (i + self.sequence_length)))
        test_energy[idx] = sample_energy.data.numpy()
        if self.details:
            encodings[idx] = enc.data.numpy()
            decodings[idx] = dec.data.numpy()
            euc_errors[idx] = z[(:, 1)].data.numpy()
            csn_errors[idx] = z[(:, 2)].data.numpy()
    test_energy = np.nanmean(test_energy, axis=0)
    if self.details:
        self.prediction_details.update({'latent_representations': np.nanmean(encodings, axis=0).T})
        self.prediction_details.update({'reconstructions_mean': np.nanmean(decodings, axis=0).T})
        self.prediction_details.update({'euclidean_errors_mean': np.nanmean(euc_errors, axis=0)})
        self.prediction_details.update({'cosine_errors_mean': np.nanmean(csn_errors, axis=0)})
    return test_energy
