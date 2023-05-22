from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import feature_map_constants as fmap_constants
import library_matching
import similarity as similarity_lib
import numpy as np
import tensorflow as tf


def np_library_matching(self, ids_predicted, ids_observed, y_predicted, y_observed, y_query):
    ids_library = np.concatenate([ids_predicted, ids_observed])
    np_library = self.np_normalize_rows(np.concatenate([y_predicted, y_observed], axis=0))
    np_similarities = np.dot(np_library, np.transpose(y_query))
    np_predictions = np.argmax(np_similarities, axis=0)
    np_predicted_ids = [ids_library[i] for i in np_predictions]
    return np_predicted_ids
