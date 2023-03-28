import itertools
import random
import unittest
from torch.utils.data.sampler import BatchSampler
from torch.utils.data.sampler import Sampler
from torch.utils.data.sampler import SequentialSampler
from torch.utils.data.sampler import RandomSampler
from maskrcnn_benchmark.data.samplers import GroupedBatchSampler
from maskrcnn_benchmark.data.samplers import IterationBasedBatchSampler


def test_len(self):
    batch_size = 3
    drop_uneven = True
    dataset = [i for i in range(10)]
    group_ids = [random.randint(0, 1) for _ in dataset]
    sampler = RandomSampler(dataset)
    batch_sampler = GroupedBatchSampler(sampler, group_ids, batch_size, drop_uneven)
    result = list(batch_sampler)
    self.assertEqual(len(result), len(batch_sampler))
    self.assertEqual(len(result), len(batch_sampler))
    batch_sampler = GroupedBatchSampler(sampler, group_ids, batch_size, drop_uneven)
    batch_sampler_len = len(batch_sampler)
    result = list(batch_sampler)
    self.assertEqual(len(result), batch_sampler_len)
    self.assertEqual(len(result), len(batch_sampler))
