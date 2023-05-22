from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from datetime import datetime
import os
import random
import sys
import threading
import numpy as np
import six
import tensorflow as tf


def _process_image_files_batch(coder, thread_index, ranges, name, filenames, synsets, labels, humans, bboxes, num_shards, logits):
    'Processes and saves list of images as TFRecord in 1 thread.\n\n  Args:\n    coder: instance of ImageCoder to provide TensorFlow image coding utils.\n    thread_index: integer, unique batch to run index is within [0, len(ranges)).\n    ranges: list of pairs of integers specifying ranges of each batches to\n      analyze in parallel.\n    name: string, unique identifier specifying the data set\n    filenames: list of strings; each string is a path to an image file\n    synsets: list of strings; each string is a unique WordNet ID\n    labels: list of integer; each integer identifies the ground truth\n    humans: list of strings; each string is a human-readable label\n    bboxes: list of bounding boxes for each image. Note that each entry in this\n      list might contain from 0+ entries corresponding to the number of bounding\n      box annotations for the image.\n    num_shards: integer number of shards for this data set.\n  '
    num_threads = len(ranges)
    assert (not (num_shards % num_threads))
    num_shards_per_batch = int((num_shards / num_threads))
    shard_ranges = np.linspace(ranges[thread_index][0], ranges[thread_index][1], (num_shards_per_batch + 1)).astype(int)
    num_files_in_thread = (ranges[thread_index][1] - ranges[thread_index][0])
    counter = 0
    for s in range(num_shards_per_batch):
        shard = ((thread_index * num_shards_per_batch) + s)
        output_filename = ('%s-%.5d-of-%.5d' % (name, shard, num_shards))
        output_file = os.path.join(FLAGS.output_directory, output_filename)
        writer = tf.python_io.TFRecordWriter(output_file)
        shard_counter = 0
        files_in_shard = np.arange(shard_ranges[s], shard_ranges[(s + 1)], dtype=int)
        for i in files_in_shard:
            filename = filenames[i]
            label = labels[i]
            synset = synsets[i]
            human = humans[i]
            bbox = bboxes[i]
            logit = logits[i]
            (image_buffer, height, width) = _process_image(filename, coder)
            example = _convert_to_example(filename, image_buffer, label, synset, human, bbox, height, width, logit)
            writer.write(example.SerializeToString())
            shard_counter += 1
            counter += 1
            if (not (counter % 1000)):
                print(('%s [thread %d]: Processed %d of %d images in thread batch.' % (datetime.now(), thread_index, counter, num_files_in_thread)))
                sys.stdout.flush()
        writer.close()
        print(('%s [thread %d]: Wrote %d images to %s' % (datetime.now(), thread_index, shard_counter, output_file)))
        sys.stdout.flush()
        shard_counter = 0
    print(('%s [thread %d]: Wrote %d images to %d shards.' % (datetime.now(), thread_index, counter, num_files_in_thread)))
    sys.stdout.flush()
