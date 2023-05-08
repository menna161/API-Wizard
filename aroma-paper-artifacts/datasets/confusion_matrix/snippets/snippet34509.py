import sys
from typing import Tuple
import numpy
from sklearn.metrics import accuracy_score, confusion_matrix


def evaluate(self, x_test: numpy.ndarray, y_test: numpy.ndarray) -> None:
    '\n        Evaluate the current model on the given test data.\n\n        Predict the labels for test data using the model and print the relevant\n        metrics like accuracy and the confusion matrix.\n\n        Args:\n            x_test (numpy.ndarray): Numpy nD array or a list like object\n                                    containing the samples.\n            y_test (numpy.ndarray): Numpy 1D array or list like object\n                                    containing the labels for test samples.\n        '
    predictions = self.predict(x_test)
    print(y_test)
    print(predictions)
    print(('Accuracy:%.3f\n' % accuracy_score(y_pred=predictions, y_true=y_test)))
    print('Confusion matrix:', confusion_matrix(y_pred=predictions, y_true=y_test))
