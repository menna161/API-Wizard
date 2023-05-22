import os as _os
import glob as _glob
import subprocess as _subprocess
import datetime as _datetime
import tarfile as _tarfile
import tempfile as _tempfile
from ._objstore import ObjectStore as objstore
from watchdog.observers import Observer as _Observer
from watchdog.events import FileSystemEventHandler as _FileSystemEventHandler


def update(self, force_upload=False):
    'Called whenever the file changes'
    if (not self._key):
        if self._rootkey:
            self._key = ('%s/%s' % (self._rootkey, self._filename))
        else:
            self._key = self._filename
        self._handle = open(self._filename, 'rb')
    while True:
        chunk = self._handle.read(self._chunksize)
        if chunk:
            if (not self._buffer):
                self._buffer = chunk
            else:
                self._buffer += chunk
            if (len(self._buffer) > self._uploadsize):
                self._uploadBuffer()
        else:
            break
    if force_upload:
        try:
            bufsize = len(self._buffer)
        except:
            bufsize = 0
        if (bufsize > 0):
            objstore.log(self._bucket, ('Uploading last of %s (%d bytes)' % (self._filename, 0)))
            self._uploadBuffer()
    elif ((_datetime.datetime.now() - self._last_upload_time).seconds > self._upload_timeout):
        self._uploadBuffer()
