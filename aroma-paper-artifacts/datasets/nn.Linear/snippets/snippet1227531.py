import tempfile
import pytest
import torch
import torch.nn as nn
from ppln.batch_processor import BaseBatchProcessor
from ppln.hooks import IterTimerHook, LogBufferHook, ProgressBarLoggerHook, TextLoggerHook
from ppln.runner import Runner


@pytest.fixture(scope='function')
def simple_runner():
    model = nn.Linear(2, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.02, momentum=0.95)
    runner = Runner(model=model, optimizer=optimizer, scheduler=None, batch_processor=SimpleBatchProcessor(), hooks=[ProgressBarLoggerHook(bar_width=10), TextLoggerHook(), IterTimerHook(), LogBufferHook()], work_dir=tempfile.mkdtemp())
    return runner
