import numpy as np
import torch
from fairseq.data import FairseqDataset, plasma_utils
from fairseq.data.token_block_utils_fast import _get_slice_indices_fast, _get_block_to_dataset_index_fast


def __init__(self, dataset, sizes, block_size, pad, eos, break_mode=None, include_targets=False, document_sep_len=1):
    try:
        from fairseq.data.token_block_utils_fast import _get_slice_indices_fast, _get_block_to_dataset_index_fast
    except ImportError:
        raise ImportError('Please build Cython components with: `pip install --editable .` or `python setup.py build_ext --inplace`')
    super().__init__()
    self.dataset = dataset
    self.pad = pad
    self.eos = eos
    self.include_targets = include_targets
    assert (len(dataset) == len(sizes))
    assert (len(dataset) > 0)
    if isinstance(sizes, list):
        sizes = np.array(sizes, dtype=np.int64)
    else:
        sizes = sizes.astype(np.int64)
    break_mode = (break_mode if (break_mode is not None) else 'none')
    if ((break_mode == 'eos') and (block_size is None)):
        block_size = 0
    slice_indices = _get_slice_indices_fast(sizes, break_mode, block_size, document_sep_len)
    self._sizes = (slice_indices[(:, 1)] - slice_indices[(:, 0)])
    if (break_mode == 'eos'):
        block_to_dataset_index = np.stack([np.arange(len(sizes)), np.zeros(len(sizes), dtype=np.long), np.arange(len(sizes))], 1)
    else:
        block_to_dataset_index = _get_block_to_dataset_index_fast(sizes, slice_indices)
    self._slice_indices = plasma_utils.PlasmaArray(slice_indices)
    self._sizes = plasma_utils.PlasmaArray(self._sizes)
    self._block_to_dataset_index = plasma_utils.PlasmaArray(block_to_dataset_index)
