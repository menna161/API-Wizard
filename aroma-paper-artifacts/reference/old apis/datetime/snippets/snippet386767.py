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


def print(self, message: str, output_datetime: bool=False, also_print: bool=None, file_logging: bool=None):
    if output_datetime:
        message = '[{0}]:{1}'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'), message)
    with self.lock_object:
        if (((file_logging is not None) and file_logging) or self.file_logging):
            if (self.log_file is None):
                self.open()
            log_file = cast(io.TextIOWrapper, self.log_file)
            log_file.write((message + '\n'))
            log_file.flush()
        if (((also_print is not None) and also_print) or self.also_print):
            print(message)
