import os
import time
import html
import threading
import sublime
from re import findall, search
from sys import platform
from subprocess import Popen, PIPE
from functools import partial
from collections import deque
from ..libraries import messages
from ..libraries.tools import prepare_command, get_setting, get_sysetting
from ..libraries.thread_progress import ThreadProgress
from .project_recognition import ProjectRecognition


def find_all_pio_errors(self, text):
    'Find PlatformIO errors\n\n        Extract all errors gived by PlatformIO\n\n        Arguments:\n            text {str} -- line string with error\n\n        Returns:\n            [tuple] -- (file_path, line_number, colum_number, error_text)\n        '
    error = []
    if ('error:' in text):
        result = search('(.+):([0-9]+):([0-9]+):\\s(.+)', text)
        if (result is not None):
            file_path = result.group(1)
            line_number = result.group(2)
            column_number = result.group(3)
            error_txt = result.group(4)
            error.append([file_path, int(line_number), int(column_number), error_txt])
    return error
