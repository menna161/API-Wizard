import argparse
import math
import numpy as np
from . import load_all
from . import show


def dataset_plots(input_file, n_theta=64, vr_max=2.5, vr_n=10, obs_length=9):
    distr = np.zeros((n_theta, vr_n))

    def fill_grid(theta_vr):
        (theta, vr) = theta_vr
        if (vr < 0.01):
            return
        thetap = math.floor(((theta * distr.shape[0]) / (2 * np.pi)))
        vrp = math.floor(((vr * distr.shape[1]) / vr_max))
        if (vrp >= distr.shape[1]):
            vrp = (distr.shape[1] - 1)
        distr[(thetap, vrp)] += 1
    unbinned_vr = [[] for _ in range(n_theta)]

    def fill_unbinned_vr(theta_vr):
        (theta, vr) = theta_vr
        if (vr < 0.01):
            return
        thetap = math.floor(((theta * len(unbinned_vr)) / (2 * np.pi)))
        unbinned_vr[thetap].append(vr)
    for (_, rows) in load_all(input_file):
        path = rows[(:, 0)]
        t_vr = compute_theta_vr(path, obs_length)
        fill_grid(t_vr)
        fill_unbinned_vr(t_vr)
    with show.canvas((input_file + '.theta.png'), figsize=(4, 4), subplot_kw={'polar': True}) as ax:
        r_edges = np.linspace(0, vr_max, (distr.shape[1] + 1))
        theta_edges = np.linspace(0, (2 * np.pi), (distr.shape[0] + 1))
        (thetas, rs) = np.meshgrid(theta_edges, r_edges)
        ax.pcolormesh(thetas, rs, distr.T, cmap='Blues')
        median_vr = np.array([(np.median(vrs) if (len(vrs) > 5) else np.nan) for vrs in unbinned_vr])
        center_thetas = np.linspace(0.0, (2 * np.pi), (len(median_vr) + 1))
        center_thetas = (0.5 * (center_thetas[:(- 1)] + center_thetas[1:]))
        center_thetas = np.hstack([center_thetas, center_thetas[0:1]])
        median_vr = np.hstack([median_vr, median_vr[0:1]])
        ax.plot(center_thetas, median_vr, label='median $v_r$ [m/s]', color='orange')
        ax.grid(linestyle='dotted')
        ax.legend()
    with show.canvas((input_file + '.speed.png'), figsize=(4, 4)) as ax:
        ax.hist([vr for theta_bin in unbinned_vr for vr in theta_bin], bins=20, range=(0.0, vr_max))
        ax.set_xlabel('$v_r$ [m/s]')
