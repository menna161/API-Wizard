import shutil
import sqlite3
import subprocess
from agnostic import AbstractBackend


def __init__(self, *args):
    super().__init__(*args)
    self._param = '?'
    self._now_fn = 'datetime()'
