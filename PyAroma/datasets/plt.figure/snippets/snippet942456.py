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


def plot_warp(warp2d, gray_image0, depth_map0, gray_image1):
    from tadataka.interpolation import interpolation
    from tadataka.coordinates import image_coordinates
    from tadataka.utils import is_in_image_range
    from matplotlib import pyplot as plt
    us0 = image_coordinates(depth_map0.shape)
    depths0 = depth_map0.flatten()
    (us1, depths1) = warp2d(us0, depths0)
    mask = is_in_image_range(us1, depth_map0.shape)
    fig = plt.figure()
    E = photometric_error(warp2d, gray_image0, depth_map0, gray_image1)
    fig.suptitle('photometric error = {:.3f}'.format(E))
    ax = fig.add_subplot(221)
    ax.set_title('t0 intensities')
    ax.imshow(gray_image0, cmap='gray')
    ax = fig.add_subplot(223)
    ax.set_title('t0 depth')
    ax.imshow(depth_map0, cmap='gray')
    ax = fig.add_subplot(222)
    ax.set_title('t1 intensities')
    ax.imshow(gray_image1, cmap='gray')
    ax = fig.add_subplot(224)
    ax.set_title('predicted t1 intensities')
    (height, width) = gray_image1.shape
    ax.scatter(us1[(mask, 0)], us1[(mask, 1)], c=gray_image0[(us0[(mask, 1)], us0[(mask, 0)])], s=0.5, cmap='gray')
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.set_aspect('equal')
    plt.show()
