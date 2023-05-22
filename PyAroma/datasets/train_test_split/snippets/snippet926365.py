from __future__ import division, print_function
import io
import logging
import os
import pprint
import numpy as np
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.pipeline import FeatureUnion
from .blocks import simple_tokenizer
from .compat import GridSearchCV, model_path, string_, train_test_split, str_cast
from .data_processing import prepare_all_data
from .util import dameraulevenshtein


def train_model(extractor, data_dir, output_dir=None):
    '\n    Train an extractor model, then write train/test block-level classification\n    performance as well as the model itself to disk in ``output_dir``.\n\n    Args:\n        extractor (:class:`Extractor`): Instance of the ``Extractor`` class to\n            be trained.\n        data_dir (str): Directory on disk containing subdirectories for all\n            training data, including raw html and gold standard blocks files\n        output_dir (str): Directory on disk to which the trained model files,\n            errors, etc. are to be written. If None, outputs are not saved.\n\n    Returns:\n        :class:`Extractor`: A trained extractor model.\n    '
    (output_dir, fname_prefix) = _set_up_output_dir_and_fname_prefix(output_dir, extractor)
    logging.info('preparing, splitting, and concatenating the data...')
    data = prepare_all_data(data_dir)
    (training_data, test_data) = train_test_split(data, test_size=0.2, random_state=42)
    (train_html, train_labels, train_weights) = extractor.get_html_labels_weights(training_data)
    (test_html, test_labels, test_weights) = extractor.get_html_labels_weights(test_data)
    logging.info('fitting and evaluating the extractor features and model...')
    try:
        extractor.fit(train_html, train_labels, weights=train_weights)
    except (TypeError, ValueError):
        extractor.fit(train_html, train_labels)
    train_eval = evaluate_model_predictions(np.concatenate(train_labels), extractor.predict(train_html), np.concatenate(train_weights))
    test_eval = evaluate_model_predictions(np.concatenate(test_labels), extractor.predict(test_html), np.concatenate(test_weights))
    _report_model_performance(output_dir, fname_prefix, train_eval, test_eval)
    _write_model_to_disk(output_dir, fname_prefix, extractor)
    return extractor
