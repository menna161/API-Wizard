import numpy as np
import sklearn.mixture
import torch
from gmm import GaussianMixture
import unittest


def testPredictClasses(self):
    '\n        Assert that torch.FloatTensor is handled correctly.\n        '
    x = torch.randn(400, 2)
    n_components = np.random.randint(1, 100)
    model = GaussianMixture(n_components, x.size(1))
    model.fit(x)
    y = model.predict(x)
    self.assertEqual(torch.Tensor(x.size(0)).size(), y.size())