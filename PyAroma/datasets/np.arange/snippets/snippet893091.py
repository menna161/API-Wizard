import copy
import logging
import numpy as np
import os
import threading
import time
from . import utils as reading_utils
import functions.artificial_generation as ag
import functions.setting.setting_utils as su


def fill(self):
    self._filled = 0
    number_of_images_per_chunk = self._number_of_images_per_chunk
    if (self._train_mode == 'Training'):
        self._fixed_im_list = self.empty_sequence(number_of_images_per_chunk)
        self._moved_im_list = self.empty_sequence(number_of_images_per_chunk)
        self._dvf_list = ([None] * number_of_images_per_chunk)
    if self._semi_epochs_completed:
        self._semi_epoch = (self._semi_epoch + 1)
        self._semi_epochs_completed = 0
        self._chunk = 0
    im_info_list_full = copy.deepcopy(self._im_info_list_full)
    random_state = np.random.RandomState(self._semi_epoch)
    if self._setting['Randomness']:
        random_indices = random_state.permutation(len(im_info_list_full))
    else:
        random_indices = np.arange(len(im_info_list_full))
    lower_range = (self._chunk * number_of_images_per_chunk)
    upper_range = ((self._chunk + 1) * number_of_images_per_chunk)
    if (upper_range >= len(im_info_list_full)):
        upper_range = len(im_info_list_full)
        self._semi_epochs_completed = 1
        number_of_images_per_chunk = (upper_range - lower_range)
        self._fixed_im_list = self.empty_sequence(number_of_images_per_chunk)
        self._moved_im_list = self.empty_sequence(number_of_images_per_chunk)
        self._dvf_list = ([None] * number_of_images_per_chunk)
    log_msg = (self._class_mode + ': stage={}, SemiEpoch={}, Chunk={} '.format(self._stage, self._semi_epoch, self._chunk))
    logging.debug(log_msg)
    if (self._class_mode == 'Thread'):
        with open(su.address_generator(self._setting, 'log_im_file'), 'a+') as f:
            f.write((log_msg + '\n'))
    torso_list = ([None] * len(self._dvf_list))
    indices_chunk = random_indices[lower_range:upper_range]
    im_info_list = [im_info_list_full[i] for i in indices_chunk]
    for (i_index_im, index_im) in enumerate(indices_chunk):
        (self._fixed_im_list[i_index_im], self._moved_im_list[i_index_im], self._dvf_list[i_index_im], torso_list[i_index_im]) = ag.get_dvf_and_deformed_images_seq(self._setting, im_info=im_info_list_full[index_im], stage_sequence=self._stage_sequence, mode_synthetic_dvf=self._mode_artificial_generation)
        if (self._class_mode == '1stEpoch'):
            self._fixed_im_list[i_index_im] = None
            self._moved_im_list[i_index_im] = None
        if self._setting['verbose']:
            log_msg = (((self._class_mode + ': Data=') + im_info_list_full[index_im]['data']) + ', TypeIm={}, CN={}, Dsmooth={}, stage={} is loaded'.format(im_info_list_full[index_im]['type_im'], im_info_list_full[index_im]['cn'], im_info_list_full[index_im]['dsmooth'], self._stage))
            logging.debug(log_msg)
            if (self._class_mode == 'Thread'):
                with open(su.address_generator(self._setting, 'log_im_file'), 'a+') as f:
                    f.write((log_msg + '\n'))
    ishuffled_folder = reading_utils.get_ishuffled_folder_write_ishuffled_setting(self._setting, self._train_mode, self._stage, self._number_of_images_per_chunk, self._samples_per_image, self._im_info_list_full, full_image=self._full_image, chunk_length_force_to_multiple_of=self._chunk_length_force_to_multiple_of)
    ishuffled_name = su.address_generator(self._setting, 'IShuffledName', semi_epoch=self._semi_epoch, chunk=self._chunk)
    ishuffled_address = (ishuffled_folder + ishuffled_name)
    if ((self._mode_artificial_generation == 'reading') and (not ((self._class_mode == 'Thread') and (self._semi_epoch > 0))) and (not self._setting['never_generate_image'])):
        count_wait = 1
        while (not os.path.isfile(ishuffled_address)):
            time.sleep(5)
            logging.debug(((self._class_mode + ': waiting {} s for IShuffled:'.format((count_wait * 5))) + ishuffled_address))
            count_wait += 1
        self._ishuffled = np.load(ishuffled_address)
    if os.path.isfile(ishuffled_address):
        self._ishuffled = np.load(ishuffled_address)
        log_msg = ((self._class_mode + ': loading IShuffled: ') + ishuffled_address)
    else:
        log_msg = ((self._class_mode + ': generating IShuffled: ') + ishuffled_address)
        self._ishuffled = reading_utils.shuffled_indices_from_chunk(self._setting, dvf_list=self._dvf_list, torso_list=torso_list, im_info_list=im_info_list, stage_sequence=self._stage_sequence, semi_epoch=self._semi_epoch, chunk=self._chunk, samples_per_image=self._samples_per_image, log_header=self._class_mode, full_image=self._full_image, seq_mode=True, chunk_length_force_to_multiple_of=self._chunk_length_force_to_multiple_of)
        np.save(ishuffled_address, self._ishuffled)
        logging.debug(((self._class_mode + ': saving IShuffled: ') + ishuffled_address))
    logging.debug(log_msg)
    if (self._class_mode == 'Thread'):
        with open(su.address_generator(self._setting, 'log_im_file'), 'a+') as f:
            f.write((log_msg + '\n'))
    if (self._class_mode == 'Thread'):
        if (not self._full_image):
            class_balanced = self._setting['ClassBalanced']
            hist_class = np.zeros(len(class_balanced), dtype=np.int32)
            hist_text = ''
            for c in range(len(class_balanced)):
                hist_class[c] = sum((self._ishuffled[(:, 2)] == c))
                hist_text = (((((hist_text + 'Class') + str(c)) + ': ') + str(hist_class[c])) + ', ')
            log_msg = ((hist_text + self._class_mode) + ': stage={}, SemiEpoch={}, Chunk={} '.format(self._stage, self._semi_epoch, self._chunk))
            with open(su.address_generator(self._setting, 'log_im_file'), 'a+') as f:
                f.write((log_msg + '\n'))
        with open(su.address_generator(self._setting, 'log_im_file'), 'a+') as f:
            f.write(('========================' + '\n'))
        logging.debug('Thread is filled .....will be paused')
        self._filled = 1
        self.pause()
