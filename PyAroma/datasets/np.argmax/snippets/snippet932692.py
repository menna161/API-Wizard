import numpy as np
import tensorflow as tf
from random import shuffle
from collections import namedtuple
from module import *
from ops import *
from utils import *
from glob import glob


def test(self, args):
    init_op = tf.global_variables_initializer()
    self.sess.run(init_op)
    sample_files_origin = glob('./test/{}2{}_{}_{}_{}/{}/npy/origin/*.*'.format(self.dataset_A_dir, self.dataset_B_dir, self.model, self.sigma_d, self.now_datetime, args.which_direction))
    sample_files_origin.sort(key=(lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[0])))
    sample_files_transfer = glob('./test/{}2{}_{}_{}_{}/{}/npy/transfer/*.*'.format(self.dataset_A_dir, self.dataset_B_dir, self.model, self.sigma_d, self.now_datetime, args.which_direction))
    sample_files_transfer.sort(key=(lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[0])))
    sample_files_cycle = glob('./test/{}2{}_{}_{}_{}/{}/npy/cycle/*.*'.format(self.dataset_A_dir, self.dataset_B_dir, self.model, self.sigma_d, self.now_datetime, args.which_direction))
    sample_files_cycle.sort(key=(lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[0])))
    sample_files = list(zip(sample_files_origin, sample_files_transfer, sample_files_cycle))
    if self.load(args.checkpoint_dir):
        print(' [*] Load SUCCESS')
    else:
        print(' [!] Load failed...')
    test_dir_mid = os.path.join(args.test_dir, '{}2{}_{}_{}_{}/{}/mid_attach_prob'.format(self.dataset_A_dir, self.dataset_B_dir, self.model, self.sigma_d, self.now_datetime, args.which_direction))
    if (not os.path.exists(test_dir_mid)):
        os.makedirs(test_dir_mid)
    count_origin = 0
    count_transfer = 0
    count_cycle = 0
    line_list = []
    for idx in range(len(sample_files)):
        print('Classifying midi: ', sample_files[idx])
        sample_origin = np.load(sample_files[idx][0])
        sample_transfer = np.load(sample_files[idx][1])
        sample_cycle = np.load(sample_files[idx][2])
        test_result_origin = self.sess.run(self.test_result_softmax, feed_dict={self.test_midi: ((sample_origin * 2.0) - 1.0)})
        test_result_transfer = self.sess.run(self.test_result_softmax, feed_dict={self.test_midi: ((sample_transfer * 2.0) - 1.0)})
        test_result_cycle = self.sess.run(self.test_result_softmax, feed_dict={self.test_midi: ((sample_cycle * 2.0) - 1.0)})
        origin_transfer_diff = np.abs((test_result_origin - test_result_transfer))
        content_diff = np.mean((((sample_origin * 1.0) - (sample_transfer * 1.0)) ** 2))
        if (args.which_direction == 'AtoB'):
            line_list.append(((idx + 1), content_diff, origin_transfer_diff[0][0], test_result_origin[0][0], test_result_transfer[0][0], test_result_cycle[0][0]))
            count_origin += (1 if (np.argmax(test_result_origin[0]) == 0) else 0)
            count_transfer += (1 if (np.argmax(test_result_transfer[0]) == 0) else 0)
            count_cycle += (1 if (np.argmax(test_result_cycle[0]) == 0) else 0)
            path_origin = os.path.join(test_dir_mid, '{}_origin_{}.mid'.format((idx + 1), test_result_origin[0][0]))
            path_transfer = os.path.join(test_dir_mid, '{}_transfer_{}.mid'.format((idx + 1), test_result_transfer[0][0]))
            path_cycle = os.path.join(test_dir_mid, '{}_cycle_{}.mid'.format((idx + 1), test_result_cycle[0][0]))
        else:
            line_list.append(((idx + 1), content_diff, origin_transfer_diff[0][1], test_result_origin[0][1], test_result_transfer[0][1], test_result_cycle[0][1]))
            count_origin += (1 if (np.argmax(test_result_origin[0]) == 1) else 0)
            count_transfer += (1 if (np.argmax(test_result_transfer[0]) == 1) else 0)
            count_cycle += (1 if (np.argmax(test_result_cycle[0]) == 1) else 0)
            path_origin = os.path.join(test_dir_mid, '{}_origin_{}.mid'.format((idx + 1), test_result_origin[0][1]))
            path_transfer = os.path.join(test_dir_mid, '{}_transfer_{}.mid'.format((idx + 1), test_result_transfer[0][1]))
            path_cycle = os.path.join(test_dir_mid, '{}_cycle_{}.mid'.format((idx + 1), test_result_cycle[0][1]))
        save_midis(sample_origin, path_origin)
        save_midis(sample_transfer, path_transfer)
        save_midis(sample_cycle, path_cycle)
    line_list.sort(key=(lambda x: x[2]), reverse=True)
    with open(os.path.join(test_dir_mid, 'Rankings_{}.txt'.format(args.which_direction)), 'w') as f:
        f.write('Id  Content_diff  P_O - P_T  Prob_Origin  Prob_Transfer  Prob_Cycle')
        for i in range(len(line_list)):
            f.writelines(('\n%5d %5f %5f %5f %5f %5f' % (line_list[i][0], line_list[i][1], line_list[i][2], line_list[i][3], line_list[i][4], line_list[i][5])))
    f.close()
    accuracy_origin = ((count_origin * 1.0) / len(sample_files))
    accuracy_transfer = ((count_transfer * 1.0) / len(sample_files))
    accuracy_cycle = ((count_cycle * 1.0) / len(sample_files))
    print('Accuracy of this classifier on test datasets is :', accuracy_origin, accuracy_transfer, accuracy_cycle)
