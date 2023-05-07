import os
import numpy as np
import objective_func.tf_models.Utils as util
from objective_func.tf_models.setup_cifar import CIFAR, CIFARModel
from objective_func.tf_models.setup_mnist import MNIST, MNISTModel
from utilities.upsampler import upsample_projection
from objective_func.tf_models.setup_inception import InceptionModel, ImageNetDataNP


def __init__(self, dataset_name, num_img=1, img_offset=0, epsilon=0.05, rescale=True, dim_reduction=None, low_dim=None, high_dim=784, obj_metric=2, results_folder=None, directory=None):
    '\n        CNN Classifier on MNIST, CIFAR10 and ImageNet\n\n        :param dataset_name: image dataset name\n        :param num_img: number of images to be attacked (default=1)\n        :param img_offset: the image id e.g. img_offset=4 means 4th image in the correctly classified test set\n        :param epsilon: maximum perturbation\n        :param rescale: rescale the adversarial image to the range of the original image\n        :param dim_reduction: dimension reduction method used in upsampling\n        :param low_dim: reduced dimension (drxdr)\n        :param high_dim: image dimension (e.g. 32x32 for CIFAR10) or high-dimensional search space for imagenet (96x96)\n        :param obj_metric: Metric used to compute objective function (default = 2)\n        :param results_folder: results saving folder directory\n        :param directory: BayesOpt Attack code directory\n        '
    self.epsilon = epsilon
    self.dataset_name = dataset_name
    self.dim_reduction = dim_reduction
    self.num_img = num_img
    self.low_dim = low_dim
    self.high_dim = high_dim
    self.objective_metric = obj_metric
    self.results_folder = results_folder
    self.rescale = rescale
    folder_path = os.path.join(directory, 'objective_func/tf_models/')
    if ('mnist' in dataset_name):
        self.d1 = 28
        self.nchannel = 1
        self.dataset_name = 'mnist'
        self.total_classes = 10
        (data, model) = (MNIST(folder_path), MNISTModel(f'{folder_path}models/mnist', use_softmax=True))
    elif ('cifar10' in dataset_name):
        self.d1 = 32
        self.nchannel = 3
        self.total_classes = 10
        self.dataset_name = 'cifar10'
        (data, model) = (CIFAR(folder_path), CIFARModel(f'{folder_path}models/cifar', use_softmax=True))
    elif ('imagenet' in dataset_name):
        from objective_func.tf_models.setup_inception import InceptionModel, ImageNetDataNP
        self.d1 = 299
        self.nchannel = 3
        self.total_classes = 1001
        self.dataset_name = 'imagenet'
        (data, model) = (ImageNetDataNP(folder_path), InceptionModel(folder_path, use_softmax=True))
    random_target = False
    shift_index = False
    attack_type = 'targeted'
    print(f'Loading data and classification model: {self.dataset_name}')
    if ('imagenet' in dataset_name):
        all_class = np.array(range(int((self.total_classes - 1))))
        (all_orig_img, all_target_labels, all_orig_labels, all_orig_img_id) = util.generate_attack_data_set(data, num_img, img_offset, model, attack_type=attack_type, random_target_class=all_class, shift_index=True)
    elif random_target:
        class_num = data.test_labels.shape[1]
        (all_orig_img, all_target_labels, all_orig_labels, all_orig_img_id) = util.generate_attack_data_set(data, num_img, img_offset, model, attack_type=attack_type, random_target_class=list(range(class_num)), shift_index=shift_index)
    else:
        (all_orig_img, all_target_labels, all_orig_labels, all_orig_img_id) = util.generate_attack_data_set(data, num_img, img_offset, model, attack_type=attack_type, shift_index=shift_index)
    self.blackbox_model = model.model
    self.all_orig_img = all_orig_img
    self.all_target_labels = all_target_labels
    self.all_orig_img_id = all_orig_img_id
    self.all_orig_labels_int = np.argmax(all_orig_labels, 1)
    if ((dataset_name == 'mnist') or (dataset_name == 'cifar10')):
        if (self.all_orig_labels_int[0] != self.all_orig_labels_int[(- 1)]):
            assert False
