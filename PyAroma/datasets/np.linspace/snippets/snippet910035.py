import numpy as np
import scipy.ndimage.filters
import skimage.measure
import collections


def ellipse(data, channels, center, a, b, theta=0, log=False, full_output=False):
    '\n    Gate that preserves events inside an ellipse-shaped region.\n\n    Events are kept if they satisfy the following relationship::\n\n        (x/a)**2 + (y/b)**2 <= 1\n\n    where `x` and `y` are the coordinates of the event list, after\n    substracting `center` and rotating by -`theta`. This is mathematically\n    equivalent to maintaining the events inside an ellipse with major\n    axis `a`, minor axis `b`, center at `center`, and tilted by `theta`.\n\n    Parameters\n    ----------\n    data : FCSData or numpy array\n        NxD flow cytometry data where N is the number of events and D is\n        the number of parameters (aka channels).\n    channels : list of int, list of str\n        Two channels on which to perform gating.\n    center, a, b, theta (optional) : float\n        Ellipse parameters. `a` is the major axis, `b` is the minor axis.\n    log : bool, optional\n        Flag specifying that log10 transformation should be applied to\n        `data` before gating.\n    full_output : bool, optional\n        Flag specifying to return additional outputs. If true, the outputs\n        are given as a namedtuple.\n\n    Returns\n    -------\n    gated_data : FCSData or numpy array\n        Gated flow cytometry data of the same format as `data`.\n    mask : numpy array of bool, only if ``full_output==True``\n        Boolean gate mask used to gate data such that ``gated_data =\n        data[mask]``.\n    contour : list of 2D numpy arrays, only if ``full_output==True``\n        List of 2D numpy array(s) of x-y coordinates tracing out\n        the edge of the gated region.\n\n    Raises\n    ------\n    ValueError\n        If more or less than 2 channels are specified.\n\n    '
    if (len(channels) != 2):
        raise ValueError('2 channels should be specified.')
    data_ch = data[(:, channels)].view(np.ndarray)
    if log:
        data_ch = np.log10(data_ch)
    center = np.array(center)
    data_centered = (data_ch - center)
    R = np.array([[np.cos(theta), np.sin(theta)], [(- np.sin(theta)), np.cos(theta)]])
    data_rotated = np.dot(data_centered, R.T)
    mask = ((((data_rotated[(:, 0)] / a) ** 2) + ((data_rotated[(:, 1)] / b) ** 2)) <= 1)
    data_gated = data[mask]
    if full_output:
        t = ((np.linspace(0, 1, 100) * 2) * np.pi)
        ci = np.array([(a * np.cos(t)), (b * np.sin(t))]).T
        ci = (np.dot(ci, R) + center)
        if log:
            ci = (10 ** ci)
        cntr = [ci]
        return EllipseGateOutput(gated_data=data_gated, mask=mask, contour=cntr)
    else:
        return data_gated
