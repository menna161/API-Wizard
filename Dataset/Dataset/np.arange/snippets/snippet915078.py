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


def __init__(self, raw_path: str, params: dict, geom):
    self._dataset_params = params
    self._timeseries_path = raw_path
    self._diskreadmda = DiskReadMda(str(self._timeseries_path))
    dtype = self._diskreadmda.dt()
    num_channels = self._diskreadmda.N1()
    sampling_frequency = float(self._dataset_params['samplerate'])
    BaseRecording.__init__(self, sampling_frequency=sampling_frequency, channel_ids=np.arange(num_channels), dtype=dtype)
    rec_segment = MdaRecordingSegment(self._diskreadmda, sampling_frequency)
    self.add_recording_segment(rec_segment)
    if (np.array(geom).ndim == 1):
        geom = [geom]
    self.set_dummy_probe_from_locations(np.array(geom))
    self._kwargs = {'raw_path': str(Path(raw_path).absolute()), 'params': params, 'geom': geom}
