from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import argparse
import sys
from datetime import datetime
from datasets import dataset_utils
from datasets import image_coder as coder
from utils import data_util
from scipy.io import loadmat
import tarfile
import subprocess
import tensorflow as tf
import numpy as np
import random


def _process_dataset(name, filenames, labels, num_shards):
    '\n  이미지 파일 목록을 읽어들여 TFRecord 객체로 변환하는 함수\n  :param name: string, 데이터 고유 문자열 (train, validation 등)\n  :param filenames: list of strings; 이미지 파일 경로 리스트.\n  :param labels: list of integer; 이미지에 대한 정수화된 정답 레이블 리스트\n  :param num_shards: 데이터 집합을 샤딩할 갯수.\n  '
    assert (len(filenames) == len(labels))
    shard_offsets = dataset_utils.make_shard_offsets(len(filenames), FLAGS.num_threads, num_shards)
    shard_output_filenames = dataset_utils.make_shard_filenames(name, len(filenames), FLAGS.num_threads, num_shards)

    def _process_batch(thread_index):
        offsets = shard_offsets[thread_index]
        output_filenames = shard_output_filenames[thread_index]
        _process_image_files_batch(thread_index, offsets, output_filenames, filenames, labels)
    dataset_utils.thread_execute(FLAGS.num_threads, _process_batch)
    dataset_utils.log(('%s: Finished writing all %d images in data set.' % (datetime.now(), len(filenames))))
