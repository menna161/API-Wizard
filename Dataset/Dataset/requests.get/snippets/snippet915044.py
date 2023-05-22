from spikeinterface.core import BaseRecording, BaseRecordingSegment, BaseSorting, BaseSortingSegment
from spikeinterface.core.core_tools import write_binary_recording
from typing import Union, List
import json
import numpy as np
from pathlib import Path
import struct
import os
import tempfile
import traceback
import requests


def _download_bytes_to_tmpfile(url, start, end):
    try:
        import requests
    except:
        raise Exception('Unable to import module: requests')
    headers = {'Range': 'bytes={}-{}'.format(start, (end - 1))}
    r = requests.get(url, headers=headers, stream=True)
    (fd, tmp_fname) = tempfile.mkstemp()
    with open(tmp_fname, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return tmp_fname
