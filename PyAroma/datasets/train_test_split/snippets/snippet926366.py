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


def train_many_models(extractor, param_grid, data_dir, output_dir=None, **kwargs):
    "\n    Train many extractor models, then for the best-scoring model, write\n    train/test block-level classification performance as well as the model itself\n    to disk in ``output_dir``.\n\n    Args:\n        extractor (:class:`Extractor`): Instance of the ``Extractor`` class to\n            be trained.\n        param_grid (dict or List[dict]): Dictionary with parameters names (str)\n            as keys and lists of parameter settings to try as values, or a list\n            of such dictionaries, in which case the grids spanned by each are\n            explored. See documentation for :class:`GridSearchCV` for details.\n        data_dir (str): Directory on disk containing subdirectories for all\n            training data, including raw html and gold standard blocks files\n        output_dir (str): Directory on disk to which the trained model files,\n            errors, etc. are to be written. If None, outputs are not saved.\n        **kwargs:\n            scoring (str or Callable): default 'f1'\n            cv (int): default 5\n            n_jobs (int): default 1\n            verbose (int): default 1\n\n    Returns:\n        :class:`Extractor`: The trained extractor model with the best-scoring\n            set of params.\n\n    See Also:\n        Documentation for grid search :class:`GridSearchCV` in ``scikit-learn``:\n            http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html\n    "
    (output_dir, fname_prefix) = _set_up_output_dir_and_fname_prefix(output_dir, extractor)
    logging.info('preparing and splitting the data...')
    data = prepare_all_data(data_dir)
    (training_data, test_data) = train_test_split(data, test_size=0.2, random_state=42)
    (train_html, train_labels, train_weights) = extractor.get_html_labels_weights(training_data)
    (test_html, test_labels, test_weights) = extractor.get_html_labels_weights(test_data)
    train_blocks = np.array([extractor.blockifier.blockify(doc) for doc in train_html])
    train_mask = [extractor._has_enough_blocks(blocks) for blocks in train_blocks]
    train_blocks = train_blocks[train_mask]
    train_labels = np.concatenate(train_labels[train_mask])
    train_weights = np.concatenate(train_weights[train_mask])
    test_labels = np.concatenate(test_labels)
    test_weights = np.concatenate(test_weights)
    train_features = np.concatenate([extractor.features.fit_transform(blocks) for blocks in train_blocks])
    gscv = GridSearchCV(extractor.model, param_grid, fit_params={'sample_weight': train_weights}, scoring=kwargs.get('scoring', 'f1'), cv=kwargs.get('cv', 5), n_jobs=kwargs.get('n_jobs', 1), verbose=kwargs.get('verbose', 1))
    gscv = gscv.fit(train_features, train_labels)
    logging.info('Score of the best model, on left-out data: %s', gscv.best_score_)
    logging.info('Params of the best model: %s', gscv.best_params_)
    extractor.model = gscv.best_estimator_
    train_eval = evaluate_model_predictions(train_labels, extractor.predict(train_html[train_mask]), weights=train_weights)
    test_eval = evaluate_model_predictions(test_labels, extractor.predict(test_html), weights=test_weights)
    _write_model_to_disk(output_dir, fname_prefix, extractor)
    return extractor
