import random
import copy
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as Fnn
import matplotlib
import matplotlib.pyplot as plt
from torch.autograd import Variable
from utils import gae, cuda_if, mean_std_groups, set_lr


def run(self, total_steps):
    ' Runs PPO\n\n        Args:\n            total_steps (int): total number of environment steps to run for\n        '
    N = self.num_workers
    T = self.worker_steps
    E = self.opt_epochs
    A = self.venv.action_space.n
    while (self.taken_steps < total_steps):
        progress = (self.taken_steps / total_steps)
        (obs, rewards, masks, actions, steps) = self.interact()
        ob_shape = obs.size()[2:]
        ep_reward = self.test()
        self.reward_histr.append(ep_reward)
        self.steps_histr.append(self.taken_steps)
        group_size = (len(self.steps_histr) // self.plot_points)
        if (self.plot_reward and ((len(self.steps_histr) % (self.plot_points * 10)) == 0) and (group_size >= 10)):
            (x_means, _, y_means, y_stds) = mean_std_groups(np.array(self.steps_histr), np.array(self.reward_histr), group_size)
            fig = plt.figure()
            fig.set_size_inches(8, 6)
            plt.ticklabel_format(axis='x', style='sci', scilimits=((- 2), 6))
            plt.errorbar(x_means, y_means, yerr=y_stds, ecolor='xkcd:blue', fmt='xkcd:black', capsize=5, elinewidth=1.5, mew=1.5, linewidth=1.5)
            plt.title('Training progress')
            plt.xlabel('Total steps')
            plt.ylabel('Episode reward')
            plt.savefig(self.plot_path, dpi=200)
            plt.clf()
            plt.close()
            plot_timer = 0
        obs_ = obs.view(((((T + 1) * N),) + ob_shape))
        obs_ = Variable(obs_)
        (_, values) = self.policy(obs_)
        values = values.view((T + 1), N, 1)
        (advantages, returns) = gae(rewards, masks, values, self.gamma, self.lambd)
        self.policy_old.load_state_dict(self.policy.state_dict())
        for e in range(E):
            self.policy.zero_grad()
            MB = (steps // self.minibatch_steps)
            b_obs = Variable(obs[:T].view(((steps,) + ob_shape)))
            b_rewards = Variable(rewards.view(steps, 1))
            b_masks = Variable(masks.view(steps, 1))
            b_actions = Variable(actions.view(steps, 1))
            b_advantages = Variable(advantages.view(steps, 1))
            b_returns = Variable(returns.view(steps, 1))
            b_inds = np.arange(steps)
            np.random.shuffle(b_inds)
            for start in range(0, steps, self.minibatch_steps):
                mb_inds = b_inds[start:(start + self.minibatch_steps)]
                mb_inds = cuda_if(torch.from_numpy(mb_inds).long(), self.cuda)
                (mb_obs, mb_rewards, mb_masks, mb_actions, mb_advantages, mb_returns) = [arr[mb_inds] for arr in [b_obs, b_rewards, b_masks, b_actions, b_advantages, b_returns]]
                (mb_pis, mb_vs) = self.policy(mb_obs)
                (mb_pi_olds, mb_v_olds) = self.policy_old(mb_obs)
                (mb_pi_olds, mb_v_olds) = (mb_pi_olds.detach(), mb_v_olds.detach())
                losses = self.objective(self.clip_func(progress), mb_pis, mb_vs, mb_pi_olds, mb_v_olds, mb_actions, mb_advantages, mb_returns)
                (policy_loss, value_loss, entropy_loss) = losses
                loss = ((policy_loss + (value_loss * self.value_coef)) + (entropy_loss * self.entropy_coef))
                set_lr(self.optimizer, self.lr_func(progress))
                self.optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm(self.policy.parameters(), self.max_grad_norm)
                self.optimizer.step()
        self.taken_steps += steps
        print(self.taken_steps)
        torch.save({'policy': self.policy.state_dict()}, (('./save/PPO_' + self.env_name) + '.pt'))
