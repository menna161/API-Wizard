import numpy as np
import sklearn.mixture
import torch
from gmm import GaussianMixture
import unittest


def testPredictProbabilities(self):
    '\n        Assert that torch.FloatTensor is handled correctly when returning class probabilities.\n        '
    x = torch.randn(400, 2)
    n_components = np.random.randint(1, 100)
    model = GaussianMixture(n_components, x.size(1))
    model.fit(x)
    y_p = model.predict(x, probs=True)
    self.assertEqual(torch.Tensor(x.size(0), n_components).size(), y_p.size())
