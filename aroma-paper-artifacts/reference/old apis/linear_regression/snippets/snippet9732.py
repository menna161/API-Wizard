import logging
import os.path
import tempfile
import unittest
import acton.database
import acton.predictors
import numpy


def test_linear_regression(self):
    'LinearRegression predictor can find a linear fit.'
    numpy.random.seed(0)
    xs = numpy.linspace(0, 1, 100)
    ys = ((2 * xs) - 1)
    noise = numpy.random.normal(size=xs.shape, scale=0.2)
    xs = xs.reshape(((- 1), 1))
    ts = (ys + noise).reshape((1, (- 1), 1))
    ids = list(range(100))
    with acton.database.ManagedHDF5Database(self.db_path) as db:
        db.write_features(ids, xs)
        db.write_labels([0], ids, ts)
        lr = acton.predictors.PREDICTORS['LinearRegression'](db)
        lr.fit(ids)
        (predictions, _variances) = lr.predict(ids)
        logging.debug('Labels: {}'.format(ys))
        logging.debug('Predictions: {}'.format(predictions))
        self.assertTrue(numpy.allclose(ys, predictions.ravel(), atol=0.2))
