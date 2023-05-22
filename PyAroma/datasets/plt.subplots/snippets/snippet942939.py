from matplotlib import pyplot as plt
from skimage.feature import plot_matches as skimage_plot_matches
from tadataka.plot.common import axis3d
from tadataka.coordinates import xy_to_yx


def plot_masked_keypoints(X, mask, true_label, false_label):
    (fig, ax) = plt.subplots()
    ax.scatter(X[(mask, 0)], X[(mask, 1)], label=true_label, color='b', marker='.')
    ax.scatter(X[((~ mask), 0)], X[((~ mask), 1)], label=false_label, color='r', marker='.')
    ax.grid(True)
    ax.legend()
    plt.show()
