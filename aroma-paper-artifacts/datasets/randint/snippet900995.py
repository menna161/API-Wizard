import copy
import random
import torch
from torch.autograd import Variable
from helper_functions import save_prediction_image, save_input_image, save_image_difference, calculate_mask_similarity, calculate_image_distance


def perform_attack(self, input_image, org_mask, target_mask, unique_class_list, total_iter=2501, save_samples=True, save_path='../adv_results/', verbose=True):
    if save_samples:
        save_prediction_image(org_mask.numpy(), 'original_mask', save_path)
        save_prediction_image(target_mask.numpy(), 'target_mask', save_path)
    self.unique_classes = unique_class_list
    self.temporary_class_id = random.randint(0, 999)
    while (self.temporary_class_id in self.unique_classes):
        self.temporary_class_id = random.randint(0, 999)
    pert_mul = self.update_perturbation_multiplier(self.beta, self.tau, 0)
    target_mask_numpy = copy.deepcopy(target_mask).numpy()
    target_mask = target_mask.float().cuda(self.device_id)
    image_to_optimize = input_image.unsqueeze(0)
    org_im_copy = copy.deepcopy(image_to_optimize.cpu()).cuda(self.device_id)
    for single_iter in range(total_iter):
        image_to_optimize = Variable(image_to_optimize.cuda(self.device_id), requires_grad=True)
        out = self.model(image_to_optimize)
        pred_out = torch.argmax(out, dim=1).float()
        l2_loss = self.calculate_l2_loss(org_im_copy, image_to_optimize)
        pred_loss = self.calculate_pred_loss(target_mask, pred_out, out)
        out_grad = torch.sum((pred_loss - l2_loss))
        out_grad.backward()
        perturbed_im = (image_to_optimize.data + (image_to_optimize.grad * pert_mul))
        perturbed_im_out = self.model(perturbed_im)
        perturbed_im_pred = torch.argmax(perturbed_im_out, dim=1).float()[0]
        perturbed_im_pred = perturbed_im_pred.detach().cpu().numpy()
        (iou, pixel_acc) = calculate_mask_similarity(perturbed_im_pred, target_mask_numpy)
        (l2_dist, linf_dist) = calculate_image_distance(org_im_copy, perturbed_im)
        pert_mul = self.update_perturbation_multiplier(self.beta, self.tau, iou)
        image_to_optimize = perturbed_im.data.clamp_(0, 1)
        if ((single_iter % 20) == 0):
            if save_samples:
                save_prediction_image(pred_out.cpu().detach().numpy()[0], ('iter_' + str(single_iter)), (save_path + 'prediction'))
                save_input_image(image_to_optimize.data.cpu().detach().numpy(), ('iter_' + str(single_iter)), (save_path + 'modified_image'))
                save_image_difference(image_to_optimize.data.cpu().detach().numpy(), org_im_copy.data.cpu().detach().numpy(), ('iter_' + str(single_iter)), (save_path + 'added_perturbation'))
            if verbose:
                print('Iter:', single_iter, '\tIOU Overlap:', iou, '\tPixel Accuracy:', pixel_acc, '\n\t\tL2 Dist:', l2_dist, '\tL_inf dist:', linf_dist)
