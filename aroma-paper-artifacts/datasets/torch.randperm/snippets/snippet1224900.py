import os
import time
import cv2
import torch
import numpy as np
import torch.utils.data as data


def _construct_new_file_names(self, length):
    assert isinstance(length, int)
    files_len = len(self._file_names)
    new_file_names = (self._file_names * (length // files_len))
    rand_indices = torch.randperm(files_len).tolist()
    new_indices = rand_indices[:(length % files_len)]
    new_file_names += [self._file_names[i] for i in new_indices]
    return new_file_names
