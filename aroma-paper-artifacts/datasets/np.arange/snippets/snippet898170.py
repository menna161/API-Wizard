import chainer
import chainer.functions as F
import numpy as np
from chainer import Variable


def _shuffle_time_order(self, video):
    frame_order = np.arange(video.shape[2])
    np.random.shuffle(frame_order)
    return video[(:, :, frame_order.tolist(), :, :)]
