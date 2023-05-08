from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import numpy as np
import argparse
import facenet
import os
import sys
import math
import pickle
from sklearn.svm import SVC


def main(args):
    with tf.Graph().as_default():
        with tf.Session() as sess:
            np.random.seed(seed=args.seed)
            if args.use_split_dataset:
                dataset_tmp = facenet.get_dataset(args.data_dir)
                (train_set, test_set) = split_dataset(dataset_tmp, args.min_nrof_images_per_class, args.nrof_train_images_per_class)
                if (args.mode == 'TRAIN'):
                    dataset = train_set
                elif (args.mode == 'CLASSIFY'):
                    dataset = test_set
            else:
                dataset = facenet.get_dataset(args.data_dir)
            for cls in dataset:
                assert ((len(cls.image_paths) > 0), 'There must be at least one image for each class in the dataset')
            (paths, labels) = facenet.get_image_paths_and_labels(dataset)
            print(('Number of classes: %d' % len(dataset)))
            print(('Number of images: %d' % len(paths)))
            print('Loading feature extraction model')
            facenet.load_model(args.model)
            images_placeholder = tf.get_default_graph().get_tensor_by_name('input:0')
            embeddings = tf.get_default_graph().get_tensor_by_name('embeddings:0')
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name('phase_train:0')
            embedding_size = embeddings.get_shape()[1]
            print('Calculating features for images')
            nrof_images = len(paths)
            nrof_batches_per_epoch = int(math.ceil(((1.0 * nrof_images) / args.batch_size)))
            emb_array = np.zeros((nrof_images, embedding_size))
            for i in range(nrof_batches_per_epoch):
                start_index = (i * args.batch_size)
                end_index = min(((i + 1) * args.batch_size), nrof_images)
                paths_batch = paths[start_index:end_index]
                images = facenet.load_data(paths_batch, False, False, args.image_size)
                feed_dict = {images_placeholder: images, phase_train_placeholder: False}
                emb_array[(start_index:end_index, :)] = sess.run(embeddings, feed_dict=feed_dict)
            classifier_filename_exp = os.path.expanduser(args.classifier_filename)
            if (args.mode == 'TRAIN'):
                print('Training classifier')
                model = SVC(kernel='linear', probability=True)
                model.fit(emb_array, labels)
                class_names = [cls.name.replace('_', ' ') for cls in dataset]
                with open(classifier_filename_exp, 'wb') as outfile:
                    pickle.dump((model, class_names), outfile)
                print(('Saved classifier model to file "%s"' % classifier_filename_exp))
            elif (args.mode == 'CLASSIFY'):
                print('Testing classifier')
                with open(classifier_filename_exp, 'rb') as infile:
                    (model, class_names) = pickle.load(infile)
                print(('Loaded classifier model from file "%s"' % classifier_filename_exp))
                predictions = model.predict_proba(emb_array)
                best_class_indices = np.argmax(predictions, axis=1)
                best_class_probabilities = predictions[(np.arange(len(best_class_indices)), best_class_indices)]
                for i in range(len(best_class_indices)):
                    print(('%4d  %s: %.3f' % (i, class_names[best_class_indices[i]], best_class_probabilities[i])))
                accuracy = np.mean(np.equal(best_class_indices, labels))
                print(('Accuracy: %.3f' % accuracy))
