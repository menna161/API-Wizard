import torch
import torch.multiprocessing as multiprocessing
from torch.utils.data.sampler import SequentialSampler, RandomSampler, BatchSampler
import collections
import sys
import traceback
import threading
import numpy as np
import numpy.random
import Queue as queue
import queue


def __init__(self, loader):
    self.dataset = loader.dataset
    self.collate_fn = loader.collate_fn
    self.batch_sampler = loader.batch_sampler
    self.num_workers = loader.num_workers
    self.pin_memory = loader.pin_memory
    self.done_event = threading.Event()
    self.sample_iter = iter(self.batch_sampler)
    if (self.num_workers > 0):
        self.index_queue = multiprocessing.SimpleQueue()
        self.data_queue = multiprocessing.SimpleQueue()
        self.batches_outstanding = 0
        self.shutdown = False
        self.send_idx = 0
        self.rcvd_idx = 0
        self.reorder_dict = {}
        self.workers = [multiprocessing.Process(target=_worker_loop, args=(self.dataset, self.index_queue, self.data_queue, self.collate_fn, np.random.randint(0, 4294967296, dtype='uint32'))) for _ in range(self.num_workers)]
        for w in self.workers:
            w.daemon = True
            w.start()
        if self.pin_memory:
            in_data = self.data_queue
            self.data_queue = queue.Queue()
            self.pin_thread = threading.Thread(target=_pin_memory_loop, args=(in_data, self.data_queue, self.done_event))
            self.pin_thread.daemon = True
            self.pin_thread.start()
        for _ in range((2 * self.num_workers)):
            self._put_indices()
