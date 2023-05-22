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


def plot_depth(image_key, pixel_age, flag_map, depth_map_true, depth_map_pred, variance_map, image_cmap='gray', depth_cmap='RdBu'):
    fig = plt.figure()
    ax = fig.add_subplot(2, 4, 1)
    ax.set_title('keyframe')
    ax.imshow(image_key, cmap=image_cmap)
    ax = fig.add_subplot(2, 4, 2)
    ax.set_title('pixel age')
    im = ax.imshow(pixel_age, cmap=image_cmap)
    plot_with_bar(ax, im)
    ax = fig.add_subplot(2, 4, 3)
    ax.set_title('flag map')
    ax.imshow(flag_to_color_map(flag_map))
    patches = [Patch('black', flag_to_rgb(f), label=f.name) for f in FLAG]
    ax.legend(handles=patches, loc='center left', bbox_to_anchor=(1.05, 0.5))
    mask = (flag_map == FLAG.SUCCESS)
    if (mask.sum() == 0):
        plt.show()
        return
    depths_pred = depth_map_pred[mask]
    depths_true = depth_map_true[mask]
    depths_diff = np.abs((depths_pred - depths_true))
    us = image_coordinates(depth_map_pred.shape)[mask.flatten()]
    vmax = np.percentile(np.concatenate((depth_map_true.flatten(), depths_pred)), 98)
    norm = Normalize(vmin=0.0, vmax=vmax)
    mapper = ScalarMappable(norm=norm, cmap=depth_cmap)
    ax = fig.add_subplot(2, 4, 5)
    ax.set_title('ground truth depth')
    ax.axis('off')
    im = ax.imshow(depth_map_true, norm=norm, cmap=depth_cmap)
    plot_with_bar(ax, im)
    (height, width) = image_key.shape[0:2]
    ax = fig.add_subplot(2, 4, 6)
    ax.set_title('predicted depth map')
    ax.axis('off')
    im = ax.imshow(image_key, cmap=image_cmap)
    ax.scatter(us[(:, 0)], us[(:, 1)], s=0.5, c=mapper.to_rgba(depths_pred))
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax = fig.add_subplot(2, 4, 7)
    ax.set_title('error = abs(pred - true)')
    im = ax.imshow(image_key, cmap=image_cmap)
    ax.scatter(us[(:, 0)], us[(:, 1)], s=0.5, c=mapper.to_rgba(depths_diff))
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax = fig.add_subplot(2, 4, 8)
    ax.set_title('variance map')
    norm = Normalize(vmin=0.0, vmax=np.percentile(variance_map.flatten(), 98))
    im = ax.imshow(variance_map, norm=norm, cmap=depth_cmap)
    plot_with_bar(ax, im)
    plt.show()
