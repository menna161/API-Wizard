from copy import deepcopy
import numpy as np
from nnunet.experiment_planning.common_utils import get_pool_and_conv_props
from nnunet.experiment_planning.experiment_planner_baseline_3DUNet import ExperimentPlanner
from nnunet.network_architecture.generic_UNet import Generic_UNet
from nnunet.paths import *


def get_target_spacing(self):
    '\n        per default we use the 50th percentile=median for the target spacing. Higher spacing results in smaller data\n        and thus faster and easier training. Smaller spacing results in larger data and thus longer and harder training\n\n        For some datasets the median is not a good choice. Those are the datasets where the spacing is very anisotropic\n        (for example ACDC with (10, 1.5, 1.5)). These datasets still have examples with a spacing of 5 or 6 mm in the low\n        resolution axis. Choosing the median here will result in bad interpolation artifacts that can substantially\n        impact performance (due to the low number of slices).\n        '
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
        if (target_spacing_of_that_axis < min(other_spacings)):
            target_spacing_of_that_axis = (max(min(other_spacings), target_spacing_of_that_axis) + 1e-05)
        target[worst_spacing_axis] = target_spacing_of_that_axis
    return target
