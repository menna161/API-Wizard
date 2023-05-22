import torch
from collections import defaultdict
from IPython import embed


def recurrent_generator(self, advantages, num_mini_batch):
    num_processes = self.rewards.size(1)
    assert (num_processes >= num_mini_batch), 'PPO requires the number of processes ({}) to be greater than or equal to the number of PPO mini batches ({}).'.format(num_processes, num_mini_batch)
    num_envs_per_batch = (num_processes // num_mini_batch)
    perm = torch.randperm(num_processes)
    for start_ind in range(0, num_processes, num_envs_per_batch):
        observations_batch = defaultdict(list)
        recurrent_hidden_states_batch = []
        actions_batch = []
        value_preds_batch = []
        return_batch = []
        masks_batch = []
        old_action_log_probs_batch = []
        adv_targ = []
        for offset in range(num_envs_per_batch):
            ind = perm[(start_ind + offset)]
            for sensor in self.observations:
                observations_batch[sensor].append(self.observations[sensor][(:(- 1), ind)])
            recurrent_hidden_states_batch.append(self.recurrent_hidden_states[(0:1, ind)])
            actions_batch.append(self.actions[(:, ind)])
            value_preds_batch.append(self.value_preds[(:(- 1), ind)])
            return_batch.append(self.returns[(:(- 1), ind)])
            masks_batch.append(self.masks[(:(- 1), ind)])
            old_action_log_probs_batch.append(self.action_log_probs[(:, ind)])
            adv_targ.append(advantages[(:, ind)])
        (T, N) = (self.num_steps, num_envs_per_batch)
        for sensor in observations_batch:
            observations_batch[sensor] = torch.stack(observations_batch[sensor], 1)
        actions_batch = torch.stack(actions_batch, 1)
        value_preds_batch = torch.stack(value_preds_batch, 1)
        return_batch = torch.stack(return_batch, 1)
        masks_batch = torch.stack(masks_batch, 1)
        old_action_log_probs_batch = torch.stack(old_action_log_probs_batch, 1)
        adv_targ = torch.stack(adv_targ, 1)
        recurrent_hidden_states_batch = torch.stack(recurrent_hidden_states_batch, 1).view(N, (- 1))
        for sensor in observations_batch:
            observations_batch[sensor] = _flatten_helper(T, N, observations_batch[sensor])
        actions_batch = _flatten_helper(T, N, actions_batch)
        value_preds_batch = _flatten_helper(T, N, value_preds_batch)
        return_batch = _flatten_helper(T, N, return_batch)
        masks_batch = _flatten_helper(T, N, masks_batch)
        old_action_log_probs_batch = _flatten_helper(T, N, old_action_log_probs_batch)
        adv_targ = _flatten_helper(T, N, adv_targ)
        (yield (observations_batch, recurrent_hidden_states_batch, actions_batch, value_preds_batch, return_batch, masks_batch, old_action_log_probs_batch, adv_targ))
