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


def __call__(self, u_key, depth_key):
    u_ref = self.warp(u_key, depth_key)
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.set_title('keyframe')
    ax.imshow(self.image_key)
    ax.scatter(u_key[0], u_key[1], c='red')
    ax = fig.add_subplot(122)
    ax.set_title('reference frame')
    ax.imshow(self.image_ref)
    ax.scatter(u_ref[0], u_ref[1], c='red')
    plt.show()
