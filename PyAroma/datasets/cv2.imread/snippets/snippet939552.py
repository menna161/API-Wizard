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


def mapf(dp):
    (fname, cls) = dp
    im = cv2.imread(fname, cv2.IMREAD_COLOR)
    im = aug.augment(im)
    return (im, cls)
