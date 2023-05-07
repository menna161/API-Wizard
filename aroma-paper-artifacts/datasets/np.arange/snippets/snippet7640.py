import numpy as np
from skimage import transform


def pixel_edges(jet_size=1.0, pixel_size=(0.1, 0.1), border_size=0.25):
    'Return pixel edges required to contain all subjets.\n\n    border_size is interpreted as a fraction of the jet_size\n    '
    im_edge = ((1.0 + border_size) * jet_size)
    return (np.arange((- im_edge), (im_edge + pixel_size[0]), pixel_size[0]), np.arange((- im_edge), (im_edge + pixel_size[1]), pixel_size[1]))
