from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import datetime
import operator
import os
import tensorflow as tf
import thumt.utils.bleu as bleu


def _evaluate(eval_fn, input_fn, decode_fn, path, config):
    graph = tf.Graph()
    with graph.as_default():
        features = input_fn()
        refs = features['references']
        placeholders = {'source': tf.placeholder(tf.int32, [None, None], 'source'), 'source_length': tf.placeholder(tf.int32, [None], 'source_length')}
        predictions = eval_fn(placeholders)
        predictions = predictions[0][(:, 0, :)]
        all_refs = [[] for _ in range(len(refs))]
        all_outputs = []
        sess_creator = tf.train.ChiefSessionCreator(checkpoint_dir=path, config=config)
        with tf.train.MonitoredSession(session_creator=sess_creator) as sess:
            while (not sess.should_stop()):
                feats = sess.run(features)
                outputs = sess.run(predictions, feed_dict={placeholders['source']: feats['source'], placeholders['source_length']: feats['source_length']})
                outputs = outputs.tolist()
                references = [item.tolist() for item in feats['references']]
                all_outputs.extend(outputs)
                for i in range(len(refs)):
                    all_refs[i].extend(references[i])
        decoded_symbols = decode_fn(all_outputs)
        decoded_refs = [decode_fn(refs) for refs in all_refs]
        decoded_refs = [list(x) for x in zip(*decoded_refs)]
        return bleu.bleu(decoded_symbols, decoded_refs)
