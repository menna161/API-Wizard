import datetime
import logging
import subprocess
from unittest import mock
from awsme.immediate_recorder import ImmediateRecorder
from awsme.metric import Metric
from awsme.buffered_recorder import BufferedRecorder, PAGE_SIZE, MAX_BATCH_SIZE, MAX_BUFFER_SIZE


def test_buffered_recorder_flush_atexit():
    completed_process = subprocess.run(['python', 'tests/buffered_recorder_atexit.py'], stdout=subprocess.PIPE, check=True)
    result = completed_process.stdout.decode()
    test_metric = Metric(event_time=datetime.datetime.min, name='1', dimensions={})
    test_result = 'Exiting\n{}\n'.format(test_metric.to_metric_data())
    assert (result == test_result)
