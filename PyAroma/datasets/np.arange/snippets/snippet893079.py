import copy
import logging
import numpy as np
import os
import threading
import time
from . import utils as reading_utils
import functions.artificial_generation as ag
import functions.setting.setting_utils as su


def generate_image_only(self):
    '\n        check if all images in self._im_info_list_full are available or generate them. Does not search for indices and create ishuffled.\n        :return:\n        '
    im_info_list_full = copy.deepcopy(self._im_info_list_full)
    random_state = np.random.RandomState(self._semi_epoch)
    if self._setting['Randomness']:
        random_indices = random_state.permutation(len(im_info_list_full))
    else:
        random_indices = np.arange(len(im_info_list_full))
    im_info_list = [im_info_list_full[i] for i in random_indices]
    for (i_im_info, im_info) in enumerate(im_info_list):
        mask_to_zero = self._setting['deform_exp'][im_info['deform_exp']]['MaskToZero']
        if (not ag.check_all_images_exist(self._setting, im_info, self._stage, mask_to_zero=mask_to_zero)):
            ag.get_dvf_and_deformed_images(self._setting, im_info=im_info, stage=self._stage, mode_synthetic_dvf=self._mode_artificial_generation)
        logging.debug((self._class_mode + ', image {}/{} is done'.format(i_im_info, len(im_info_list))))
    logging.debug((self._class_mode + ': generate_image_only exiting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .'))
