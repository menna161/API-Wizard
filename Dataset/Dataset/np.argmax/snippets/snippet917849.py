import shutil
from collections import OrderedDict
from copy import deepcopy
import nnunet
import numpy as np
from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.configuration import default_num_threads
from nnunet.experiment_planning.DatasetAnalyzer import DatasetAnalyzer
from nnunet.experiment_planning.common_utils import get_pool_and_conv_props_poolLateV2
from nnunet.experiment_planning.utils import create_lists_from_splitted_dataset
from nnunet.network_architecture.generic_UNet import Generic_UNet
from nnunet.paths import *
from nnunet.preprocessing.cropping import get_case_identifier_from_npz
from nnunet.training.model_restore import recursive_find_python_class
import argparse


def get_target_spacing(self):
    spacings = self.dataset_properties['all_spacings']
    'worst_spacing_axis = np.argmax(target)\n        if max(target) > (2.5 * min(target)):\n            spacings_of_that_axis = np.vstack(spacings)[:, worst_spacing_axis]\n            target_spacing_of_that_axis = np.percentile(spacings_of_that_axis, 5)\n            target[worst_spacing_axis] = target_spacing_of_that_axis'
    target = np.percentile(np.vstack(spacings), self.target_spacing_percentile, 0)
    return target
