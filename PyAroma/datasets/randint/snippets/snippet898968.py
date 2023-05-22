from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import feature_map_constants as fmap_constants
import library_matching
import similarity as similarity_lib
import numpy as np
import tensorflow as tf


def testCosineSimilarityProviderMatching(self):
    'Check correctness for querying the library with a library element.'
    num_examples = 20
    num_trials = 10
    data_dim = 5
    similarity = similarity_lib.CosineSimilarityProvider()
    library = np.float32(np.random.normal(size=(num_examples, data_dim)))
    library = tf.constant(library)
    library = similarity.preprocess_library(library)
    query_idx = tf.placeholder(shape=(), dtype=tf.int32)
    query = library[query_idx][(np.newaxis, ...)]
    (match_idx_op, match_similarity_op, _, _, _) = library_matching._max_similarity_match(library, query, similarity)
    with tf.Session() as sess:
        for _ in range(num_trials):
            idx = np.random.randint(0, high=num_examples)
            (match_idx, match_similarity) = sess.run([match_idx_op, match_similarity_op], feed_dict={query_idx: idx})
            if (match_idx != idx):
                self.assertClose(match_similarity, 1.0)
