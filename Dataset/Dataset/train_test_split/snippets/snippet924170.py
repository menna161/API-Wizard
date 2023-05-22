import logging
import numpy as np
from sklearn.model_selection import train_test_split
from models import Model
from models import optimize


def fit(self, X, Y, T, max_iter=2000):
    (X, X_val, Y, Y_val, T, T_val) = train_test_split(X, Y, T, test_size=0.1, stratify=Y)
    idx = np.argsort(T)
    X = X[idx]
    Y = Y[idx]
    T = T[idx]
    self.t = T
    d = X.shape[1]
    self.w = np.zeros((d, 1))
    f_old = np.inf
    loss_fn = (lambda w: self.loss(w, X, Y, self.H))
    for i in range(max_iter):
        self.H = self.cumulative_h(X, Y)
        (self.w, self.f) = optimize(loss_fn, self.w)
        print(f'Iteration {i}: 	 train loss: {(self.f / len(T)):.4f} 	 val error: {self.evaluate(X_val, Y_val, T_val):.4f}')
        if (abs((self.f - f_old)) < 0.001):
            break
        f_old = self.f
