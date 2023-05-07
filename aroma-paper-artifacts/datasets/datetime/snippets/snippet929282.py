from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from concurrent import futures
import collections
import datetime
import itertools
import json
import pathlib
import re
import uuid
import numpy as np
import tensorflow as tf


def _random_filename(self, extension):
    timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    identifier = str(uuid.uuid4()).replace('-', '')
    filename = '{}-{}.{}'.format(timestamp, identifier, extension)
    return filename
