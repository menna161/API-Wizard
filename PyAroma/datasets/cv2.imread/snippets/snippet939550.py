import multiprocessing as mp
import numpy as np
from abc import abstractmethod
import cv2
import tensorflow as tf
from tensorpack import imgaug, dataset, ModelDesc
from tensorpack.dataflow import BatchData, MultiThreadMapData, DataFromList, AugmentImageComponent, MultiProcessRunnerZMQ
from tensorpack.models import regularize_cost
from tensorpack.predict import FeedfreePredictor, PredictConfig
from tensorpack.tfutils.summary import add_moving_summary
from tensorpack.tfutils.optimizer import AccumGradOptimizer
from tensorpack.utils import logger
from tensorpack.utils.stats import RatioCounter


def get_val_dataflow(datadir, batch_size, augmentors=None, parallel=None, num_splits=None, split_index=None):
    if (augmentors is None):
        augmentors = fbresnet_augmentor(False)
    assert (datadir is not None)
    assert isinstance(augmentors, list)
    if (parallel is None):
        parallel = min(40, mp.cpu_count())
    if (num_splits is None):
        ds = dataset.ILSVRC12Files(datadir, 'val', shuffle=False)
    else:
        assert (split_index < num_splits)
        files = dataset.ILSVRC12Files(datadir, 'val', shuffle=False)
        files.reset_state()
        files = list(files.get_data())
        logger.info('Number of validation data = {}'.format(len(files)))
        split_size = (len(files) // num_splits)
        (start, end) = ((split_size * split_index), (split_size * (split_index + 1)))
        end = min(end, len(files))
        logger.info('Local validation split = {} - {}'.format(start, end))
        files = files[start:end]
        ds = DataFromList(files, shuffle=False)
    aug = imgaug.AugmentorList(augmentors)

    def mapf(dp):
        (fname, cls) = dp
        im = cv2.imread(fname, cv2.IMREAD_COLOR)
        im = aug.augment(im)
        return (im, cls)
    ds = MultiThreadMapData(ds, parallel, mapf, buffer_size=min(2000, ds.size()), strict=True)
    ds = BatchData(ds, batch_size, remainder=True)
    return ds
