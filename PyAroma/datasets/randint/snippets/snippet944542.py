import numpy as np
from fairseq.data import data_utils
from . import BaseWrapperDataset


def __getitem__(self, index):
    with data_utils.numpy_seed(self.seed, self.epoch, index):
        item = self.dataset[index]
        item_len = item.size(0)
        excess = (item_len - self.truncation_length)
        if (excess > 0):
            start_idx = np.random.randint(0, excess)
            item = item[start_idx:(start_idx + self.truncation_length)]
        return item
