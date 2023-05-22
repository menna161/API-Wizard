import os
import threading
from vision_case.model import VisionDensenetModel, VisionResNetModel, DIR_PATH
from service_streamer import ThreadedStreamer, ManagedModel, Streamer, RedisStreamer, RedisWorker, run_redis_workers_forever
import torch
import pytest


def init_model(self):
    self.model = VisionResNetModel(device=device)
