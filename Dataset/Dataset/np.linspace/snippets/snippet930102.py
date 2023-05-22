from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import gzip
import os
import shutil
import ssl
import sys
import tarfile
import threading
import zipfile
from datetime import datetime
import numpy as np
import tensorflow as tf
from six.moves import urllib


def split_range(total, num_split, start_index=0):
    '\n  정수 범위의 값을 num_split 값만큼 분할하여 해당 start, end 인덱스를 반환.\n  :param total: 분할하고자 하는 max 값\n  :param num_split: 분할 갯수\n  :param start_index: contents 시작 인덱스 번호로 default 값으로 0을 사용\n  :return: split 갯수 크기의 리스트로 start/end 인덱스 튜플을 원소로 가짐.  [(s,e),(s,e),...]\n  '
    rs = np.linspace(start_index, total, (num_split + 1)).astype(np.int)
    result = [(rs[i], rs[(i + 1)]) for i in range((len(rs) - 1))]
    return result
