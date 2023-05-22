import numpy as np
import random
import copy


def revert_coordinate_space(channels, R0, T0):
    (n, d) = channels.shape
    channels_rec = copy.copy(channels)
    (R_prev, T_prev) = (R0, T0)
    rootRotInd = np.arange(3, 6)
    for ii in range(n):
        R_diff = expmap2rotmat(channels[(ii, rootRotInd)])
        R = R_diff.dot(R_prev)
        channels_rec[(ii, rootRotInd)] = rotmat2expmap(R)
        T = (T_prev + R_prev.T.dot(np.reshape(channels[(ii, :3)], [3, 1])).reshape((- 1)))
        channels_rec[(ii, :3)] = T
        (T_prev, R_prev) = (T, R)
    return channels_rec
