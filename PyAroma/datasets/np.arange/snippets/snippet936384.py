import numpy as np


def __fit_precomputed_kernel(self, X, y):
    '\n        Fits an estimator of p(s=1|x) and estimates the value of p(s=1|y=1) using a subset of the training examples\n\n        X -- Precomputed kernel matrix\n        y -- Labels associated to each example in X (Positive label: 1.0, Negative label: -1.0)\n        '
    positives = np.where((y == 1.0))[0]
    hold_out_size = np.ceil((len(positives) * self.hold_out_ratio))
    if (len(positives) <= hold_out_size):
        raise (('Not enough positive examples to estimate p(s=1|y=1,x). Need at least ' + str((hold_out_size + 1))) + '.')
    np.random.shuffle(positives)
    hold_out = positives[:hold_out_size]
    X_test_hold_out = X[hold_out]
    keep = list((set(np.arange(len(y))) - set(hold_out)))
    X_test_hold_out = X_test_hold_out[(:, keep)]
    X = X[(:, keep)]
    X = X[keep]
    y = np.delete(y, hold_out)
    self.estimator.fit(X, y)
    hold_out_predictions = self.estimator.predict_proba(X_test_hold_out)
    try:
        hold_out_predictions = hold_out_predictions[(:, 1)]
    except:
        pass
    c = np.mean(hold_out_predictions)
    self.c = c
    self.estimator_fitted = True
