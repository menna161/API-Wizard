import threading
import subprocess
import time
import os
import math
import random
import io
from queue import Queue
from enum import Enum
from enum import IntEnum
from datetime import datetime
from typing import Optional, Union, cast
from typing import List, Tuple, Dict


def open(self):
    self.close()
    if (not os.path.exists(self.log_folder)):
        os.mkdir(self.log_folder)
    with Log.static_lock_object:
        count = Log.static_count
        Log.static_count += 1
    filename = 'log{0}_{1}.txt'.format(datetime.now().strftime('%Y-%m-%d %H-%M-%S'), count)
    self.log_filename = os.path.join(self.log_folder, filename)
    self.log_file = open(self.log_filename, 'w', encoding='utf_8_sig')
