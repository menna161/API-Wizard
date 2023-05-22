from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import atexit
import multiprocessing
import os
import tempfile
import uuid
import numpy as np
import six
import tensorflow as tf


def iter_shard_dataframe(df, rows_per_core=1000):
    'Two way shard of a dataframe.\n\n  This function evenly shards a dataframe so that it can be mapped efficiently.\n  It yields a list of dataframes with length equal to the number of CPU cores,\n  with each dataframe having rows_per_core rows. (Except for the last batch\n  which may have fewer rows in the dataframes.) Passing vectorized inputs to\n  a multiprocessing pool is much more effecient than iterating through a\n  dataframe in serial and passing a list of inputs to the pool.\n\n  Args:\n    df: Pandas dataframe to be sharded.\n    rows_per_core: Number of rows in each shard.\n\n  Returns:\n    A list of dataframe shards.\n  '
    n = len(df)
    num_cores = min([multiprocessing.cpu_count(), n])
    num_blocks = int(np.ceil(((n / num_cores) / rows_per_core)))
    max_batch_size = (num_cores * rows_per_core)
    for i in range(num_blocks):
        min_index = (i * max_batch_size)
        max_index = min([((i + 1) * max_batch_size), n])
        df_shard = df[min_index:max_index]
        n_shard = len(df_shard)
        boundaries = np.linspace(0, n_shard, (num_cores + 1), dtype=np.int64)
        (yield [df_shard[boundaries[j]:boundaries[(j + 1)]] for j in range(num_cores)])
