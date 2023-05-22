import logging
import torch
from typing import List
from pytorch_transformers import *
from service_streamer import ManagedModel


def init_model(self):
    self.model = TextInfillingModel()
