from matplotlib import pyplot as plt
from skimage.feature import plot_matches as skimage_plot_matches
from tadataka.plot.common import axis3d
from tadataka.coordinates import xy_to_yx


def plot_masked_points(P, mask, true_label, false_label):
    ax = axis3d()
    ax.scatter(P[(mask, 0)], P[(mask, 1)], P[(mask, 2)], 'b.', label=true_label)
    ax.scatter(P[((~ mask), 0)], P[((~ mask), 1)], P[((~ mask), 2)], 'r.', label=false_label)
    ax.legend()
    plt.show()
