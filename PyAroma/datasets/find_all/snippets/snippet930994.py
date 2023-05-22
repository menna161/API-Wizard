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


def _on_data(self, data):
    try:
        characters = data.decode(self.encoding)
    except:
        characters = (('[Decode error - output not ' + self.encoding) + ']\n')
    if (not self._txt):
        if (not self._output):
            self._output = characters
        else:
            self._output += characters
        return
    characters = characters.replace('\r\n', '\n').replace('\r', '\n')
    self._txt.print(characters)
    if self.show_errors_inline:
        errors = self.find_all_pio_errors(characters)
        for (file, line, column, text) in errors:
            if (file not in self.errs_by_file):
                self.errs_by_file[file] = []
            self.errs_by_file[file].append((line, column, text))
        self.update_phantoms()
