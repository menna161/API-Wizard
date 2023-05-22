import logging
import torch
from typing import List
from pytorch_transformers import *
from service_streamer import ManagedModel

if (__name__ == '__main__'):
    batch = ['twinkle twinkle [MASK] star.', 'Happy birthday to [MASK].', 'the answer to life, the [MASK], and everything.']
    model = TextInfillingModel()
    outputs = model.predict(batch)
    print(outputs)
