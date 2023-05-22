import os as _os
import glob as _glob
import subprocess as _subprocess
import datetime as _datetime
import tarfile as _tarfile
import tempfile as _tempfile
from ._objstore import ObjectStore as objstore
from watchdog.observers import Observer as _Observer
from watchdog.events import FileSystemEventHandler as _FileSystemEventHandler


def _uploadBuffer(self):
    'Internal function that uploads the current buffer to\n           a new chunk in the object store'
    if (self._buffer is None):
        return
    elif (len(self._buffer) == 0):
        return
    self._next_chunk += 1
    self._last_upload_time = _datetime.datetime.now()
    objstore.log(self._bucket, ('Upload %s chunk (%f KB) to %s/%s' % (self._filename, (float(len(self._buffer)) / 1024.0), self._key, self._next_chunk)))
    objstore.set_object(self._bucket, ('%s/%d' % (self._key, self._next_chunk)), self._buffer)
    self._buffer = None
