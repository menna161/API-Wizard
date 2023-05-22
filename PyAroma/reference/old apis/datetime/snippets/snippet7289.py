import os as _os
import glob as _glob
import subprocess as _subprocess
import datetime as _datetime
import tarfile as _tarfile
import tempfile as _tempfile
from ._objstore import ObjectStore as objstore
from watchdog.observers import Observer as _Observer
from watchdog.events import FileSystemEventHandler as _FileSystemEventHandler


def __init__(self, filename, bucket, rootkey, sizetrigger, timetrigger):
    self._filename = filename
    self._bucket = bucket
    self._rootkey = rootkey
    self._handle = None
    self._key = None
    self._buffer = None
    self._last_upload_time = _datetime.datetime.now()
    self._next_chunk = 0
    self._chunksize = 8192
    self._uploadsize = int(sizetrigger)
    self._upload_timeout = int(timetrigger)
