import os
import numpy as np
import objective_func.tf_models.Utils as util
from objective_func.tf_models.setup_cifar import CIFAR, CIFARModel
from objective_func.tf_models.setup_mnist import MNIST, MNISTModel
from utilities.upsampler import upsample_projection
from objective_func.tf_models.setup_inception import InceptionModel, ImageNetDataNP


def get_data_sample(self, i=0):
    '\n        :param i: the attack target label id\n        '
    if (i > (self.total_classes - 2)):
        assert False
    self.X_origin = self.all_orig_img[i:(i + 1)]
    self.orig_img_id = self.all_orig_img_id[i:(i + 1)][0]
    self.input_label = self.all_orig_labels_int[i:(i + 1)][0]
    X_orig_img_file = os.path.join(self.results_folder, f'X_{self.dataset_name}_origin_{self.input_label}_id{self.orig_img_id}')
    if ('imagenet' in self.dataset_name):
        np.save(X_orig_img_file, np.array([0]))
    else:
        np.save(X_orig_img_file, self.X_origin)
    target_label_vector = self.all_target_labels[i:(i + 1)]
    self.target_label = np.argmax(target_label_vector, 1)
