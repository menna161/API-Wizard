import logging
import os
import os.path
import shutil
import sys
from datetime import datetime
from six.moves import input
from termcolor import colored
from .fs import mkdir_p


def _get_time_str():
    return datetime.now().strftime('%m%d-%H%M%S')
