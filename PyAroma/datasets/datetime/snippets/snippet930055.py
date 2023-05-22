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


def _process_image_files(name, filenames, synsets, labels, humans, bboxes, num_shards, logits):
    'Process and save list of images as TFRecord of Example protos.\n\n  Args:\n    name: string, unique identifier specifying the data set\n    filenames: list of strings; each string is a path to an image file\n    synsets: list of strings; each string is a unique WordNet ID\n    labels: list of integer; each integer identifies the ground truth\n    humans: list of strings; each string is a human-readable label\n    bboxes: list of bounding boxes for each image. Note that each entry in this\n      list might contain from 0+ entries corresponding to the number of bounding\n      box annotations for the image.\n    num_shards: integer number of shards for this data set.\n  '
    assert (len(filenames) == len(synsets))
    assert (len(filenames) == len(labels))
    assert (len(filenames) == len(humans))
    assert (len(filenames) == len(bboxes))
    spacing = np.linspace(0, len(filenames), (FLAGS.num_threads + 1)).astype(np.int)
    ranges = []
    threads = []
    for i in range((len(spacing) - 1)):
        ranges.append([spacing[i], spacing[(i + 1)]])
    print(('Launching %d threads for spacings: %s' % (FLAGS.num_threads, ranges)))
    sys.stdout.flush()
    coord = tf.train.Coordinator()
    coder = ImageCoder()
    threads = []
    for thread_index in range(len(ranges)):
        args = (coder, thread_index, ranges, name, filenames, synsets, labels, humans, bboxes, num_shards, logits)
        t = threading.Thread(target=_process_image_files_batch, args=args)
        t.start()
        threads.append(t)
    coord.join(threads)
    print(('%s: Finished writing all %d images in data set.' % (datetime.now(), len(filenames))))
    sys.stdout.flush()
