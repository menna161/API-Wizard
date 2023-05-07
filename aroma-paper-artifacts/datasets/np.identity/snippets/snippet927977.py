import numpy as np
from ..utils import metrics


def fit(self, X):
    '\n        Auguments\n        ---------\n            X: ndarray, the event count matrix of shape num_instances-by-num_events\n        '
    print('====== Model summary ======')
    (num_instances, num_events) = X.shape
    X_cov = (np.dot(X.T, X) / float(num_instances))
    (U, sigma, V) = np.linalg.svd(X_cov)
    n_components = self.n_components
    if (n_components < 1):
        total_variance = np.sum(sigma)
        variance = 0
        for i in range(num_events):
            variance += sigma[i]
            if ((variance / total_variance) >= n_components):
                break
        n_components = (i + 1)
    P = U[(:, :n_components)]
    I = np.identity(num_events, int)
    self.components = P
    self.proj_C = (I - np.dot(P, P.T))
    print('n_components: {}'.format(n_components))
    print('Project matrix shape: {}-by-{}'.format(self.proj_C.shape[0], self.proj_C.shape[1]))
    if (not self.threshold):
        phi = np.zeros(3)
        for i in range(3):
            for j in range(n_components, num_events):
                phi[i] += np.power(sigma[j], (i + 1))
        h0 = (1.0 - (((2 * phi[0]) * phi[2]) / ((3.0 * phi[1]) * phi[1])))
        self.threshold = (phi[0] * np.power(((((self.c_alpha * np.sqrt((((2 * phi[1]) * h0) * h0))) / phi[0]) + 1.0) + (((phi[1] * h0) * (h0 - 1)) / (phi[0] * phi[0]))), (1.0 / h0)))
    print('SPE threshold: {}\n'.format(self.threshold))
