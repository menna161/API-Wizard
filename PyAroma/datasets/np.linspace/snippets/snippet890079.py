import pandas as pd, numpy as np
from dataclasses import dataclass, replace
from axcell.models.linking.metrics import CM
from matplotlib import pyplot as plt
import matplotlib.tri as tri


def threshold_map(self, metric):
    lin = np.linspace(0, 1, 64)
    triang = tri.Triangulation(self.results.threshold1.values, self.results.threshold2.values)
    interpolator = tri.LinearTriInterpolator(triang, self.results[metric])
    (Xi, Yi) = np.meshgrid(lin, lin)
    zi = interpolator(Xi, Yi)
    plt.figure(figsize=(6, 6))
    img = plt.imshow(zi[::(- 1)], extent=[0, 1, 0, 1])
    plt.colorbar(img)
    plt.xlabel('threshold1')
    plt.ylabel('threshold2')
