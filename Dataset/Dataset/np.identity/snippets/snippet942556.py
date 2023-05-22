import warnings
import numpy as np
from scipy.spatial.transform import Rotation
from sparseba import SBA, can_run_ba
from tadataka.rigid_transform import transform
from tadataka.pose import Pose
from tadataka.transform_project import pose_jacobian, point_jacobian, transform_project


def update_weights(robustifier, x_true, x_pred, weights):
    E = calc_errors(x_true, x_pred, weights)
    I = np.identity(2)
    return np.array([(I * w) for w in robustifier.weights(E)])
