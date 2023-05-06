import os
import numpy as np
import objective_func.tf_models.Utils as util
from objective_func.tf_models.setup_cifar import CIFAR, CIFARModel
from objective_func.tf_models.setup_mnist import MNIST, MNISTModel
from utilities.upsampler import upsample_projection
from objective_func.tf_models.setup_inception import InceptionModel, ImageNetDataNP


def evaluate(self, delta_vector):
    '\n        :param delta_vector: adversarial perturbation in the range of [-epsilon, epsilon]\n        :return score:  = log_p_max - log_p_target [N] if obj_metric=1;\n                        = log_sum_{j \not target} p_j - log_p_target [N] if obj_metric=2 (default)\n                        both to be minimised\n        '
    delta = delta_vector.reshape((- 1), self.d1, self.d1, self.nchannel)
    X_adv = (self.X_origin.copy() + delta)
    if self.rescale:
        X_adv = (X_adv / (1 + (2 * self.epsilon)))
    else:
        X_adv = X_adv.clip((- 0.5), 0.5)
    prob_all_labels = self.blackbox_model.predict(X_adv)
    prob_all_labels = np.atleast_2d(prob_all_labels)
    log_prob_all_labels = np.log((prob_all_labels + 1e-30))
    log_p_target = log_prob_all_labels[(:, self.target_label)]
    log_p_predicted_label = np.max(log_prob_all_labels, 1)
    predicted_labels = np.argmax(log_prob_all_labels, 1)
    if (self.objective_metric == 1):
        score = (log_p_predicted_label[(:, None)] - log_p_target)
    elif (self.objective_metric == 2):
        p_target_labels = prob_all_labels[(:, self.target_label)]
        sum_p_other_labels = (np.sum(prob_all_labels, 1)[(:, None)] - p_target_labels)
        log_sum_p_other_labels = np.log((sum_p_other_labels + 1e-30))
        score = (log_sum_p_other_labels - log_p_target)
    all_queries_success = (predicted_labels == self.target_label)
    if (all_queries_success.sum() > 0):
        self.success = True
        score = (- 1)
        X_success_adv = X_adv[(predicted_labels == self.target_label)]
        print(f'attack succeed! || origin={self.input_label}| target={self.target_label[0]}')
        X_success_saving_path = os.path.join(self.results_folder, f'X_{self.dataset_name}_adv_i{self.input_label}_t{self.target_label[0]}_eps{self.epsilon}_id{self.orig_img_id}')
        if ('imagenet' in self.dataset_name):
            np.save(X_success_saving_path, np.array([0]))
        else:
            np.save(X_success_saving_path, X_success_adv)
    else:
        self.success = False
        print(f'attack succeed={False}|| origin={self.input_label}| target={self.target_label[0]}|min score at targer={score}| predicted={predicted_labels}')
    return score
