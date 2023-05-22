import os
import threading
from vision_case.model import VisionDensenetModel, VisionResNetModel, DIR_PATH
from service_streamer import ThreadedStreamer, ManagedModel, Streamer, RedisStreamer, RedisWorker, run_redis_workers_forever
import torch
import pytest


def setup_class(self):
    with open(os.path.join(DIR_PATH, 'cat.jpg'), 'rb') as f:
        image_bytes = f.read()
    self.input_batch = [image_bytes]
    self.vision_model = VisionDensenetModel(device=device)
    self.single_output = self.vision_model.batch_prediction(self.input_batch)
    self.batch_output = self.vision_model.batch_prediction((self.input_batch * BATCH_SIZE))
    with open(os.path.join(DIR_PATH, 'dog.jpg'), 'rb') as f:
        image_bytes2 = f.read()
    self.input_batch2 = [image_bytes2]
    self.vision_model2 = VisionResNetModel(device=device)
    self.single_output2 = self.vision_model2.batch_prediction(self.input_batch2)
    self.batch_output2 = self.vision_model2.batch_prediction((self.input_batch2 * BATCH_SIZE))
    self.managed_model = ManagedVisionDensenetModel()
    self.managed_model.init_model()
