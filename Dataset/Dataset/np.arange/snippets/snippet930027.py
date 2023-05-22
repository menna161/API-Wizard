from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import random
import argparse
import sys
from datetime import datetime
from datasets import dataset_utils
from datasets import image_coder as coder
from utils import data_util
import tensorflow as tf
import numpy as np


def _process_image_files_batch(thread_index, offsets, output_filenames, filenames, labels, bbox_info):
    '\n  하나의 스레드 단위에서 이미지 리스트를 읽어 TRRecord 타입으로 변환하는 함수\n  :param thread_index: 현재 작업중인 thread 번호.\n  :param offsets: offset list. 이미지 목록 중 현재 스레드에서 처리해야 할 offset 값으로 shard 갯수만큼 리스트로 제공\n  :param output_filenames: 출력 파일 이름으로 shard 갯수만큼 리스트로 제공.\n  :param filenames: 처리해야 할 전체 이미지 파일 리스트\n  :param labels: 처리해야 할 전체 이미지 레이블 리스트\n  '
    assert (len(offsets) == len(output_filenames))
    assert (len(filenames) == len(labels))
    num_files_in_thread = (offsets[(- 1)][1] - offsets[0][0])
    counter = 0
    for (offset, output_filename) in zip(offsets, output_filenames):
        output_file = os.path.join(FLAGS.output_dir, output_filename)
        writer = tf.python_io.TFRecordWriter(output_file)
        files_in_shard = np.arange(offset[0], offset[1], dtype=int)
        shard_counter = 0
        for i in files_in_shard:
            filename = filenames[i]
            label = labels[i]
            file_id = os.path.splitext(os.path.basename(filename))[0]
            if (bbox_info is None):
                bbox = None
            else:
                bbox = bbox_info[file_id]
            (image_data, height, width, image_format) = _process_image(filename, bbox)
            example = data_util.convert_to_example_without_bbox(image_data, 'jpg', label, height, width)
            writer.write(example.SerializeToString())
            counter += 1
            shard_counter += 1
            if (not (counter % 1000)):
                dataset_utils.log(('%s [thread %2d]: Processed %d of %d images in thread batch.' % (datetime.now(), thread_index, counter, num_files_in_thread)))
        writer.close()
        dataset_utils.log(('%s [thread %2d]: Wrote %d images to %s' % (datetime.now(), thread_index, shard_counter, output_file)))
