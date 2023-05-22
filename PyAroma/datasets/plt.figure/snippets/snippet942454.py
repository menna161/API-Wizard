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


def plot_prior(image, depth_map_true, depth_map_pred, variance_map_pred, image_cmap='gray', depth_cmap='RdBu'):
    fig = plt.figure()
    fig.suptitle('Prior')
    vmin = min(np.min(depth_map_true), np.min(depth_map_pred))
    vmax = max(np.max(depth_map_true), np.max(depth_map_pred))
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    mapper = ScalarMappable(norm=norm, cmap=depth_cmap)
    ax = fig.add_subplot(221)
    ax.set_title('frame')
    ax.imshow(image, cmap=image_cmap)
    ax = fig.add_subplot(222)
    ax.set_title('ground truth depth map')
    im = ax.imshow(depth_map_true, norm=norm, cmap=depth_cmap)
    ax = fig.add_subplot(223)
    ax.set_title('prior depth map')
    im = ax.imshow(depth_map_pred, norm=norm, cmap=depth_cmap)
    plot_with_bar(ax, im)
    ax = fig.add_subplot(224)
    ax.set_title('prior variance map')
    im = ax.imshow(variance_map_pred, cmap=depth_cmap)
    plot_with_bar(ax, im)
    plt.show()
