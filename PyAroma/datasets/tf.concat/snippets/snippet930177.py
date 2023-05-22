from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import numpy as np
import tensorflow as tf
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import normalize


def recall_at_k(flags_obj, flags_core, input_function_eval, model_for_eval, num_val_images, return_embedding=False, eval_similarity='cosine'):
    datasets = input_function_eval(is_training=False, data_dir=flags_obj.data_dir, batch_size=int(flags_obj.val_batch_size), num_epochs=1, dct_method=flags_obj.dct_method, dataset_name=flags_obj.dataset_name, dtype=flags_core.get_tf_dtype(flags_obj), preprocessing_type=flags_obj.preprocessing_type, val_regex=flags_obj.val_regex)
    one_shot_iter = datasets.make_one_shot_iterator()
    image_and_label = one_shot_iter.get_next()
    num_gpus = 1
    input_images = image_and_label[0]
    batch_size = tf.shape(input_images)[0]
    mod_val = tf.mod(batch_size, num_gpus)
    input_images = tf.cond(tf.equal(mod_val, 0), (lambda : input_images), (lambda : tf.concat([input_images, input_images[:(num_gpus - mod_val)]], axis=0)))
    split_input_images = tf.split(input_images, num_gpus, axis=0)
    embedding_list = []
    for i in range(num_gpus):
        with tf.device(('/gpu:%d' % i)):
            if return_embedding:
                embedding = model_for_eval(split_input_images[i], False, use_resnet_d=flags_obj.use_resnet_d, return_embedding=True)
                tf.logging.info('Evaluation using Embedding')
            else:
                embedding = model_for_eval(split_input_images[i], False, use_resnet_d=flags_obj.use_resnet_d)
            tf.get_variable_scope().reuse_variables()
            embedding_list.append(embedding)
    embedding = tf.concat(embedding_list, axis=0)[:batch_size]
    if (flags_obj.dtype == 'fp32'):
        ph_query = tf.placeholder(tf.float32, shape=[None, None], name='ph_query')
        ph_index = tf.placeholder(tf.float32, shape=[None, None], name='ph_index')
    else:
        ph_query = tf.placeholder(tf.float16, shape=[None, None], name='ph_query')
        ph_index = tf.placeholder(tf.float16, shape=[None, None], name='ph_index')
    k_list = flags_obj.recall_at_k
    query_size = tf.shape(ph_query)[0]
    batch_size = tf.shape(ph_index)[0]
    mod_val = tf.mod(batch_size, num_gpus)
    if (flags_obj.dtype == 'fp32'):
        dummy_features = tf.zeros([(num_gpus - mod_val), tf.shape(ph_index)[1]])
    else:
        dummy_features = tf.zeros([(num_gpus - mod_val), tf.shape(ph_index)[1]], dtype=tf.float16)
    index_features = tf.cond(tf.equal(mod_val, 0), (lambda : ph_index), (lambda : tf.concat([ph_index, dummy_features], axis=0)))
    split_index_features = tf.split(index_features, num_gpus, axis=0)
    check_split = tf.shape(split_index_features[0])[0]
    split_top_k_indices_list = []
    split_top_k_values_list = []
    if (eval_similarity == 'cosine'):
        l2_query = tf.nn.l2_normalize(ph_query, axis=1)
    for i in range(num_gpus):
        with tf.device(('/gpu:%d' % i)):
            if (eval_similarity == 'cosine'):
                l2_index = tf.nn.l2_normalize(split_index_features[i], axis=1)
                split_mat = tf.matmul(l2_query, l2_index, transpose_b=True)
            elif (eval_similarity == 'euclidean'):
                split_mat = (- tf_simple_pairwise_distance(ph_query, split_index_features[i]))
            else:
                raise NotImplementedError
            (split_top_k_values, split_top_k_indices) = tf.nn.top_k(split_mat, k=(np.max(k_list) + 1), sorted=True)
            split_top_k_indices += (i * check_split)
            split_top_k_values_list.append(split_top_k_values)
            split_top_k_indices_list.append(split_top_k_indices)
    pre_top_k_indices = tf.concat(split_top_k_indices_list, axis=1)
    pre_top_k_values = tf.concat(split_top_k_values_list, axis=1)
    (post_top_k_values, post_top_k_indices) = tf.nn.top_k(pre_top_k_values, k=(np.max(k_list) + 1), sorted=True)
    (ii, _) = tf.meshgrid(tf.range(query_size, dtype=tf.int32), tf.range((np.max(k_list) + 1), dtype=tf.int32), indexing='ij')
    indices = tf.stack([ii, post_top_k_indices], axis=(- 1))
    top_k_indices = tf.gather_nd(pre_top_k_indices, indices)
    saver = tf.train.Saver()
    if tf.gfile.IsDirectory(flags_obj.model_dir):
        checkpoint_path = tf.train.latest_checkpoint(flags_obj.model_dir)
    else:
        checkpoint_path = flags_obj.model_dir
    np_features = np.zeros((num_val_images, int(embedding.get_shape()[1])), dtype=np.float32)
    np_labels = np.zeros(num_val_images, dtype=np.int64)
    np_i = 0
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, checkpoint_path)
        while True:
            try:
                (np_predict, np_label) = sess.run([embedding, image_and_label[1]])
                np_features[(np_i:(np_i + np_predict.shape[0]), :)] = np_predict
                np_labels[np_i:(np_i + np_label.shape[0])] = np_label
                np_i += np_predict.shape[0]
            except tf.errors.OutOfRangeError:
                break
        assert (np_i == num_val_images)
        not_dist_idx = (np_labels != (- 1))
        dist_idx = np.logical_not(not_dist_idx)
        np_query = np_features[not_dist_idx]
        np_query_labels = np_labels[not_dist_idx]
        np_dist = np_features[dist_idx]
        np_dist_labels = np_labels[dist_idx]
        sorted_idx = get_sorted_idx(np_query, np_features, sess, ph_query, ph_index, top_k_indices)
    recall_dict = get_recall(sorted_idx, np_query_labels, np_labels, k_list)
    for key in recall_dict.keys():
        tf.summary.scalar(('recall_at_%d' % key), tf.constant(recall_dict[key]))
    merged = tf.summary.merge_all()
    test_writer = tf.summary.FileWriter((flags_obj.model_dir + '/eval'))
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        summary = sess.run(merged)
        global_step = int(os.path.basename(checkpoint_path).split('-')[1])
        test_writer.add_summary(summary, global_step)
    eval_results = {}
    for key in recall_dict.keys():
        eval_results[('recall_at_%d' % key)] = recall_dict[key]
    eval_results['global_step'] = global_step
    return eval_results
