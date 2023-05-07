from __future__ import division
import os
import time
from shutil import copyfile
from glob import glob
import tensorflow as tf
import numpy as np
import config
from collections import namedtuple
from module import *
from utils import *
from ops import *
from metrics import *


def test(self, args):
    init_op = tf.global_variables_initializer()
    self.sess.run(init_op)
    if (args.which_direction == 'AtoB'):
        sample_files = glob('./datasets/{}/test/*.*'.format(self.dataset_A_dir))
    elif (args.which_direction == 'BtoA'):
        sample_files = glob('./datasets/{}/test/*.*'.format(self.dataset_B_dir))
    else:
        raise Exception('--which_direction must be AtoB or BtoA')
    sample_files.sort(key=(lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[(- 1)])))
    if self.load(args.checkpoint_dir):
        print(' [*] Load SUCCESS')
    else:
        print(' [!] Load failed...')
    if (args.which_direction == 'AtoB'):
        (out_origin, out_var, out_var_cycle, in_var) = (self.test_A_binary, self.testB_binary, self.testA__binary, self.test_A)
    else:
        (out_origin, out_var, out_var_cycle, in_var) = (self.test_B_binary, self.testA_binary, self.testB__binary, self.test_B)
    test_dir_mid = os.path.join(args.test_dir, '{}2{}_{}_{}_{}/{}/mid'.format(self.dataset_A_dir, self.dataset_B_dir, self.now_datetime, self.model, self.sigma_d, args.which_direction))
    if (not os.path.exists(test_dir_mid)):
        os.makedirs(test_dir_mid)
    test_dir_npy = os.path.join(args.test_dir, '{}2{}_{}_{}_{}/{}/npy'.format(self.dataset_A_dir, self.dataset_B_dir, self.now_datetime, self.model, self.sigma_d, args.which_direction))
    if (not os.path.exists(test_dir_npy)):
        os.makedirs(test_dir_npy)
    for idx in range(len(sample_files)):
        print('Processing midi: ', sample_files[idx])
        sample_npy = (np.load(sample_files[idx]) * 1.0)
        sample_npy_re = sample_npy.reshape(1, sample_npy.shape[0], sample_npy.shape[1], 1)
        midi_path_origin = os.path.join(test_dir_mid, '{}_origin.mid'.format((idx + 1)))
        midi_path_transfer = os.path.join(test_dir_mid, '{}_transfer.mid'.format((idx + 1)))
        midi_path_cycle = os.path.join(test_dir_mid, '{}_cycle.mid'.format((idx + 1)))
        (origin_midi, fake_midi, fake_midi_cycle) = self.sess.run([out_origin, out_var, out_var_cycle], feed_dict={in_var: sample_npy_re})
        save_midis(origin_midi, midi_path_origin)
        save_midis(fake_midi, midi_path_transfer)
        save_midis(fake_midi_cycle, midi_path_cycle)
        npy_path_origin = os.path.join(test_dir_npy, 'origin')
        npy_path_transfer = os.path.join(test_dir_npy, 'transfer')
        npy_path_cycle = os.path.join(test_dir_npy, 'cycle')
        if (not os.path.exists(npy_path_origin)):
            os.makedirs(npy_path_origin)
        if (not os.path.exists(npy_path_transfer)):
            os.makedirs(npy_path_transfer)
        if (not os.path.exists(npy_path_cycle)):
            os.makedirs(npy_path_cycle)
        np.save(os.path.join(npy_path_origin, '{}_origin.npy'.format((idx + 1))), origin_midi)
        np.save(os.path.join(npy_path_transfer, '{}_transfer.npy'.format((idx + 1))), fake_midi)
        np.save(os.path.join(npy_path_cycle, '{}_cycle.npy'.format((idx + 1))), fake_midi_cycle)
