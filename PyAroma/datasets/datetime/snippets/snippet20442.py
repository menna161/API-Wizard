from __future__ import unicode_literals
import base64
import codecs
import datetime
import distutils.util
from email import message_from_file
import hashlib
import imp
import json
import logging
import os
import posixpath
import re
import shutil
import sys
import tempfile
import zipfile
from . import __version__, DistlibException
from .compat import sysconfig, ZipFile, fsdecode, text_type, filter
from .database import InstalledDistribution
from .metadata import Metadata, METADATA_FILENAME, WHEEL_METADATA_FILENAME
from .util import FileOperator, convert_path, CSVReader, CSVWriter, Cache, cached_property, get_cache_base, read_exports, tempdir
from .version import NormalizedVersion, UnsupportedVersionError


def _get_extensions(self):
    pathname = os.path.join(self.dirname, self.filename)
    name_ver = ('%s-%s' % (self.name, self.version))
    info_dir = ('%s.dist-info' % name_ver)
    arcname = posixpath.join(info_dir, 'EXTENSIONS')
    wrapper = codecs.getreader('utf-8')
    result = []
    with ZipFile(pathname, 'r') as zf:
        try:
            with zf.open(arcname) as bf:
                wf = wrapper(bf)
                extensions = json.load(wf)
                cache = self._get_dylib_cache()
                prefix = cache.prefix_to_dir(pathname)
                cache_base = os.path.join(cache.base, prefix)
                if (not os.path.isdir(cache_base)):
                    os.makedirs(cache_base)
                for (name, relpath) in extensions.items():
                    dest = os.path.join(cache_base, convert_path(relpath))
                    if (not os.path.exists(dest)):
                        extract = True
                    else:
                        file_time = os.stat(dest).st_mtime
                        file_time = datetime.datetime.fromtimestamp(file_time)
                        info = zf.getinfo(relpath)
                        wheel_time = datetime.datetime(*info.date_time)
                        extract = (wheel_time > file_time)
                    if extract:
                        zf.extract(relpath, cache_base)
                    result.append((name, dest))
        except KeyError:
            pass
    return result
