import datetime
import logging
import subprocess
from unittest import mock
from awsme.immediate_recorder import ImmediateRecorder
from awsme.metric import Metric
from awsme.buffered_recorder import BufferedRecorder, PAGE_SIZE, MAX_BATCH_SIZE, MAX_BUFFER_SIZE


def make_recorder(dimensions_count):
    fake_recorder = mock.Mock(spec=ImmediateRecorder)
    recorder = BufferedRecorder(recorder=fake_recorder)
    recorder.put_metric(Metric(datetime.datetime.utcnow(), 'test', {str(number): str(number) for number in range(dimensions_count)}))
    return (recorder, fake_recorder)
