from .multi_registry import register
from sklearn.svm import LinearSVC
from .base_model import BaseModel
import os
import pickle


@register('svm')
def instatiate_svm(params, **kwargs):
    '\n        Returns a RF wrapped by the PU Learning Adapter.\n    '
    hparms = {'penalty': 'l2', 'dual': False, 'tol': 0.1}
    hparms.update(kwargs)
    wrapped_svm = SVMWrapper(LinearSVC(**hparms), params)
    return wrapped_svm
