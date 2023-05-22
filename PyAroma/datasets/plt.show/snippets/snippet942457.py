import numpy as np
import matplotlib
from matplotlib.cm import ScalarMappable
from matplotlib.patches import Patch
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize, CSS4_COLORS, to_rgb
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D
from tadataka.metric import photometric_error
from tadataka.rigid_transform import Transform
from tadataka.rigid_motion import LeastSquaresRigidMotion
from tadataka.vo.semi_dense.flag import ResultFlag as FLAG
from tadataka.coordinates import image_coordinates
from tadataka.interpolation import interpolation
from tadataka.coordinates import image_coordinates
from tadataka.utils import is_in_image_range
from matplotlib import pyplot as plt


def plot_trajectory(trajectory_true, trajectory_pred):
    (R, t, s) = LeastSquaresRigidMotion(trajectory_pred, trajectory_true).solve()
    trajectory_pred = Transform(R, t, s)(trajectory_pred)
    print('MSE: ', np.power((trajectory_pred - trajectory_true), 2).mean())
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(trajectory_pred[(:, 0)], trajectory_pred[(:, 1)], trajectory_pred[(:, 2)], label='pred')
    ax.plot(trajectory_true[(:, 0)], trajectory_true[(:, 1)], trajectory_true[(:, 2)], label='true')
    plt.legend()
    plt.show()
