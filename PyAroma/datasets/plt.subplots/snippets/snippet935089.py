import math
import numpy as np
import collections
from matplotlib import collections as mc
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


def plot_ori(self, c):
    from matplotlib import collections as mc
    import matplotlib.pyplot as plt
    line_len = 1
    lines = [[(p[0], p[1]), ((p[0] + (line_len * self._angles[p][0])), (p[1] + (line_len * self._angles[p][1])))] for p in self._nodes]
    lc = mc.LineCollection(lines, linewidth=2, color='green')
    (_, ax) = plt.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    xs = [p[0] for p in self._nodes]
    ys = [p[1] for p in self._nodes]
    plt.scatter(xs, ys, color=c)
