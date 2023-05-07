import numpy as np
from itertools import product, combinations
import mcubes as libmcubes
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
import seaborn as sns
from trimesh.path.creation import box_outline
from trimesh.path.util import concatenate
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib


def draw_voxel_model(voxels, is_show=True, save_path=None):
    import matplotlib.pyplot as plt
    if (not is_show):
        import matplotlib
        matplotlib.use('Agg')
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.colors import LightSource
    import seaborn as sns
    color_num = voxels.max()
    current_palette = sns.color_palette(as_cmap=True)
    colors = np.empty(voxel.shape, dtype=object)
    for i in range(color_num):
        colors[(voxel == (i + 1))] = current_palette[i]
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(voxels, facecolors=colors, lightsource=LightSource(azdeg=315, altdeg=45))
    if is_show:
        plt.show()
    if (save_path is not None):
        plt.savefig(save_path, transparent=True)
