from scipy.interpolate import CubicSpline, CubicHermiteSpline
import airsimneurips as airsim
import cvxpy as cp
import numpy as np
import time


def __init__(self, gate_poses):
    self.gates = gate_poses
    self.n_gates = np.size(gate_poses, 0)
    positions = np.array([pose.position.to_numpy_array() for pose in gate_poses])
    dists = np.linalg.norm((positions[(1:, :)] - positions[(:(- 1), :)]), axis=1)
    self.arc_length = np.zeros(shape=self.n_gates)
    self.arc_length[1:] = np.cumsum(dists)
    self.tangents = np.zeros(shape=(self.n_gates, 3))
    for (i, pose) in enumerate(gate_poses):
        self.tangents[(i, :)] = rotate_vector(pose.orientation, gate_facing_vector).to_numpy_array()
    self.track_spline = CubicHermiteSpline(self.arc_length, positions, self.tangents, axis=0)
    gate_widths = [(gate_dimensions[0] / 2.0) for gate in gate_poses]
    gate_heights = [(gate_dimensions[1] / 2.0) for gate in gate_poses]
    self.track_width_spline = CubicSpline(self.arc_length, gate_widths, axis=0)
    self.track_height_spline = CubicSpline(self.arc_length, gate_heights, axis=0)
    taus = np.linspace(self.arc_length[0], self.arc_length[(- 1)], (2 ** 12))
    self.track_centers = self.track_spline(taus)
    self.track_tangents = self.track_spline.derivative(nu=1)(taus)
    self.track_tangents /= np.linalg.norm(self.track_tangents, axis=1)[(:, np.newaxis)]
    self.track_normals = np.zeros_like(self.track_tangents)
    self.track_normals[(:, 0)] = (- self.track_tangents[(:, 1)])
    self.track_normals[(:, 1)] = self.track_tangents[(:, 0)]
    self.track_normals /= np.linalg.norm(self.track_normals, axis=1)[(:, np.newaxis)]
    self.track_widths = self.track_width_spline(taus)
    self.track_heights = self.track_height_spline(taus)
