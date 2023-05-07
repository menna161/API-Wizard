import pydrr
import pydrr.autoinit
import SimpleITK as sitk
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1
import numpy as np
import sys
from pydrr import utils


def main():
    if (len(sys.argv) < 2):
        print('rendering.py <volume path>')
        return
    mhd_filename = sys.argv[1]
    (volume, spacing) = load_image(mhd_filename)
    print(pydrr.get_supported_kernels())
    print(pydrr.get_current_kernel())
    pydrr.set_current_kernel('render_with_cubic_interp')
    print(pydrr.get_current_kernel())
    volume = pydrr.utils.HU2Myu((volume - 1000), 0.2683)
    (pm_Nx3x4, image_size, image_spacing) = load_test_projection_matrix()
    T_Nx4x4 = load_test_transform_matrix()
    volume_context = pydrr.VolumeContext(volume.astype(np.float32), spacing)
    geometry_context = pydrr.GeometryContext()
    geometry_context.projection_matrix = pm_Nx3x4
    n_channels = (T_Nx4x4.shape[0] * pm_Nx3x4.shape[0])
    detector = pydrr.Detector(pydrr.Detector.make_detector_size(image_size, n_channels), image_spacing)
    projector = pydrr.Projector(detector, 1.0).to_gpu()
    t_volume_context = volume_context.to_texture()
    d_image = projector.project(t_volume_context, geometry_context, T_Nx4x4)
    image = d_image.get()
    print('Result image shape:', image.shape)
    plt.figure(figsize=(16, 9))
    n_show_channels = 3
    for i in range(min(image.shape[2], n_show_channels)):
        ax = plt.subplot(1, min(image.shape[2], n_show_channels), (i + 1))
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(ax)
        cax = divider.append_axes('right', '5%', pad='3%')
        im = ax.imshow(image[(:, :, i)], interpolation='none', cmap='gray')
        plt.colorbar(im, cax=cax)
    plt.show()
    save_image('drr.mhd', image, image_spacing)
