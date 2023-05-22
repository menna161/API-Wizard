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


def log(msg, *args):
    msg = ('[{}] ' + msg)
    print(msg.format(datetime.now(), *args))
    sys.stdout.flush()
