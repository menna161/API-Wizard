import numpy as np


def rings(level_y):
    thetas = np.linspace(0, (2 * np.pi), (point_density + 1))[:(- 1)]
    inner = (inner_r * round_points(thetas))
    outer = (outer_r * round_points(thetas))
    inner[(:, 1)] = level_y
    outer[(:, 1)] = level_y
    return np.vstack((inner, outer))
