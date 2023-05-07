import numpy as np
import sklearn.mixture
import torch
from gmm import GaussianMixture
import unittest


def testEmMatchesFullSkLearn(self):
    '\n        Assert that log-probabilities (E-step) and parameter updates (M-step) approximately match those of sklearn.\n        '
    d = 20
    n_components = np.random.randint(1, 100)
    x = torch.randn(400, 1, d).double()
    x_np = np.squeeze(x.data.numpy())
    var_init = torch.eye(d, dtype=torch.float64).reshape(1, 1, d, d).repeat(1, n_components, 1, 1)
    model = GaussianMixture(n_components, d, init_params='random', var_init=var_init, covariance_type='full')
    model_sk = sklearn.mixture.GaussianMixture(n_components, covariance_type='full', init_params='random', means_init=np.squeeze(model.mu.data.numpy()), precisions_init=np.squeeze(np.linalg.inv(var_init)))
    model_sk._initialize_parameters(x_np, np.random.RandomState())
    log_prob_sk = model_sk._estimate_log_prob(x_np)
    log_prob = model._estimate_log_prob(x)
    np.testing.assert_almost_equal(np.squeeze(log_prob.data.numpy()), log_prob_sk, decimal=2, verbose=True)
    (_, log_resp_sk) = model_sk._e_step(x_np)
    (_, log_resp) = model._e_step(x)
    np.testing.assert_almost_equal(np.squeeze(log_resp.data.numpy()), log_resp_sk, decimal=0, verbose=True)
    model_sk._m_step(x_np, log_resp_sk)
    pi_sk = model_sk.weights_
    mu_sk = model_sk.means_
    var_sk = model_sk.covariances_
    (pi, mu, var) = model._m_step(x, log_resp)
    np.testing.assert_almost_equal(np.squeeze(pi.data.numpy()), pi_sk, decimal=1, verbose=True)
    np.testing.assert_almost_equal(np.squeeze(mu.data.numpy()), mu_sk, decimal=1, verbose=True)
    np.testing.assert_almost_equal(np.squeeze(var.data.numpy()), var_sk, decimal=1, verbose=True)
