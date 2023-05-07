import numpy as np
import matplotlib.pyplot as plt
import functions.setting.setting_utils as su
import SimpleITK as sitk


def view3d_image(input_im, cmap='gray', title='', spacing=None, slice_axis=0):
    if (spacing is None):
        spacing = [1, 1, 1]
    if isinstance(input_im, sitk.Image):
        input_numpy = sitk.GetArrayFromImage(input_im)
        spacing = input_im.GetSpacing()[::(- 1)]
    else:
        input_numpy = input_im
    if (slice_axis == 0):
        aspect = (spacing[1] / spacing[2])
    elif (slice_axis == 1):
        input_numpy = np.transpose(input_numpy, [1, 0, 2])
        aspect = (spacing[0] / spacing[2])
    elif (slice_axis == 2):
        input_numpy = np.transpose(input_numpy, [2, 0, 1])
        aspect = (spacing[0] / spacing[1])
    else:
        raise ValueError((('slice_axis = ' + str(slice_axis)) + ', but it should be in range of [0, 1, 2]'))
    (fig, ax) = plt.subplots(1, 1)
    tracker = IndexTracker(ax, input_numpy, cmap=cmap, title=title, aspect=aspect)
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    plt.show()
