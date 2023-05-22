from matplotlib import pyplot as plt
from skimage.feature import plot_matches as skimage_plot_matches
from tadataka.plot.common import axis3d
from tadataka.coordinates import xy_to_yx


def plot_matches(image0, image1, keypoints0, keypoints1, matches01):
    (fig, ax) = plt.subplots()
    skimage_plot_matches(ax, image0, image1, xy_to_yx(keypoints0), xy_to_yx(keypoints1), matches01)
