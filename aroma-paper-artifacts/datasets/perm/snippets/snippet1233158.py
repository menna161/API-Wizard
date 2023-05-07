import mask_reconstructor
import numpy as np
from nabu.postprocessing import data_reader
import itertools


def _get_masks_opt_frame_perm(self, output, target, utt_info):
    'estimate the masks\n\n\t\tArgs:\n\t\t\toutput: the output of a single utterance of the neural network\n\t\t\ttarget: the target of a single utterance of the neural network\n\t\t\tutt_info: some info on the utterance\n\n\t\tReturns:\n\t\t\tthe estimated masks'
    (usedbins, _) = self.usedbins_reader(self.pos)
    [T, F] = np.shape(usedbins)
    masks = self._get_masks(output, utt_info)
    target = target['multi_targets']
    target = np.reshape(target, [T, F, self.nrS])
    target = np.transpose(target, [2, 0, 1])
    target = np.abs(target)
    sum_targets = np.sum(target, axis=0, keepdims=True)
    irms = (target / sum_targets)
    usedbins_ext = np.expand_dims(usedbins, 0)
    opt_masks = np.zeros([self.nrS, T, F])
    all_perms = list(itertools.permutations(range(self.nrS)))
    for t in range(T):
        mask_frame_t = masks[(:, t, :)]
        irms_frame_t = irms[(:, t, :)]
        usedbins_frame_t = usedbins_ext[(:, t, :)]
        perm_values = np.zeros([self.nrS])
        for (perm_ind, perm) in enumerate(all_perms):
            perm_value = np.sum((usedbins_frame_t * np.abs((mask_frame_t[(perm, :)] - irms_frame_t))))
            perm_values[perm_ind] = perm_value
        best_perm_ind = np.argmin(perm_values)
        best_perm = all_perms[best_perm_ind]
        opt_masks[(:, t, :)] = mask_frame_t[(best_perm, :)]
    return opt_masks
