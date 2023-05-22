import argparse
import numpy as np
from . import load_all
from . import show
from . import Reader
from .interactions import non_linear, leader_follower, collision_avoidance, group
from .interactions import check_interaction, interaction_length


def distribution_plots(input_file, args):
    (n_theta, vr_n, dist_thresh, choice) = (args.n_theta, args.vr_n, args.dist_thresh, args.choice)
    distr = np.zeros((n_theta, vr_n))

    def fill_grid(theta_vr):
        (theta, vr) = theta_vr
        theta = ((theta * (2 * np.pi)) / 360)
        thetap = np.floor(((theta * distr.shape[0]) / (2 * np.pi))).astype(int)
        vrp = np.floor(((vr * distr.shape[1]) / dist_thresh)).astype(int)
        distr[(thetap, vrp)] += 1
    unbinned_vr = [[] for _ in range(n_theta)]

    def fill_unbinned_vr(theta_vr):
        (theta, vr) = theta_vr
        theta = ((theta * (2 * np.pi)) / 360)
        thetap = np.floor(((theta * len(unbinned_vr)) / (2 * np.pi))).astype(int)
        for (th, _) in enumerate(thetap):
            unbinned_vr[thetap[th]].append(vr[th])
    vr_max = dist_thresh
    hist = []

    def fill_hist(vel):
        hist.append(vel)
    for (_, rows) in load_all(input_file):
        (_, chosen_true, dist_true) = check_interaction(rows, pos_range=args.pos_range, dist_thresh=args.dist_thresh, choice=args.choice, pos_angle=args.pos_angle, vel_angle=args.vel_angle, vel_range=args.vel_range, output='all', obs_len=args.obs_len)
        fill_grid((chosen_true, dist_true))
        fill_unbinned_vr((chosen_true, dist_true))
        fill_hist(chosen_true)
    with show.canvas((((input_file + '.') + choice) + '.png'), figsize=(4, 4), subplot_kw={'polar': True}) as ax:
        r_edges = np.linspace(0, vr_max, (distr.shape[1] + 1))
        theta_edges = np.linspace(0, (2 * np.pi), (distr.shape[0] + 1))
        (thetas, rs) = np.meshgrid(theta_edges, r_edges)
        ax.pcolormesh(thetas, rs, distr.T, vmin=0, vmax=None, cmap='Blues')
        median_vr = np.array([(np.median(vrs) if (len(vrs) > 5) else np.nan) for vrs in unbinned_vr])
        center_thetas = np.linspace(0.0, (2 * np.pi), (len(median_vr) + 1))
        center_thetas = (0.5 * (center_thetas[:(- 1)] + center_thetas[1:]))
        center_thetas = np.hstack([center_thetas, center_thetas[0:1]])
        median_vr = np.hstack([median_vr, median_vr[0:1]])
        ax.grid(linestyle='dotted')
        ax.legend()
    with show.canvas((((input_file + '.') + choice) + '_hist.png'), figsize=(4, 4)) as ax:
        ax.hist(np.hstack(hist), bins=n_theta)
