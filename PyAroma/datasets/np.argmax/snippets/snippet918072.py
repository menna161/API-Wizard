import numpy as np
from nnunet.experiment_planning.experiment_planner_baseline_3DUNet_v21 import ExperimentPlanner3D_v21
from nnunet.paths import *


def get_target_spacing(self):
    spacings = self.dataset_properties['all_spacings']
    sizes = self.dataset_properties['all_sizes']
    target = np.percentile(np.vstack(spacings), self.target_spacing_percentile, 0)
    target_size = np.percentile(np.vstack(sizes), self.target_spacing_percentile, 0)
    target_size_mm = (np.array(target) * np.array(target_size))
    worst_spacing_axis = np.argmax(target)
    other_axes = [i for i in range(len(target)) if (i != worst_spacing_axis)]
    other_spacings = [target[i] for i in other_axes]
    other_sizes = [target_size[i] for i in other_axes]
    has_aniso_spacing = (target[worst_spacing_axis] > (self.anisotropy_threshold * min(other_spacings)))
    has_aniso_voxels = ((target_size[worst_spacing_axis] * self.anisotropy_threshold) < min(other_sizes))
    if (has_aniso_spacing and has_aniso_voxels):
        spacings_of_that_axis = np.vstack(spacings)[(:, worst_spacing_axis)]
        target_spacing_of_that_axis = np.percentile(spacings_of_that_axis, 10)
        target_spacing_of_that_axis = max((min(other_spacings) * self.anisotropy_threshold), target_spacing_of_that_axis)
        target[worst_spacing_axis] = target_spacing_of_that_axis
    return target
