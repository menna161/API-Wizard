import os.path as osp
import sys
from amazing_brick.game.wrapped_amazing_brick import GameState
from amazing_brick.game.amazing_brick_utils import CONST
from DQN_train.gym_wrapper import AmazingBrickEnv3
import tianshou as ts
import torch, numpy as np
from torch import nn
import torch.nn.functional as F
import json
import datetime

if (__name__ == '__main__'):
    try:
        with open((dqn3_path + 'dqn3_log.json'), 'r') as f:
            jlist = json.load(f)
        log_dict = jlist[(- 1)]
        round = log_dict['round']
        policy.load_state_dict(torch.load((((dqn3_path + 'dqn3round_') + str(int(round))) + '.pth')))
        del jlist
    except FileNotFoundError as identifier:
        print('\n\nWe shall train a bright new net.\n')
        with open((dqn3_path + 'dqn3_log.json'), 'a+') as f:
            f.write('[]')
            round = 0
    while True:
        round += 1
        print('\n\nround:{}\n\n'.format(round))
        result = ts.trainer.offpolicy_trainer(policy, train_collector, test_collector, max_epoch=max_epoch, step_per_epoch=step_per_epoch, collect_per_step=collect_per_step, episode_per_test=30, batch_size=64, train_fn=(lambda e1, e2: policy.set_eps((0.1 / round))), test_fn=(lambda e1, e2: policy.set_eps((0.05 / round))), writer=None)
        print(f"Finished training! Use {result['duration']}")
        torch.save(policy.state_dict(), (((dqn3_path + 'dqn3round_') + str(int(round))) + '.pth'))
        policy.load_state_dict(torch.load((((dqn3_path + 'dqn3round_') + str(int(round))) + '.pth')))
        log_dict = {}
        log_dict['round'] = round
        log_dict['last_train_time'] = datetime.datetime.now().strftime('%y-%m-%d %I:%M:%S %p %a')
        log_dict['best_reward'] = result['best_reward']
        with open((dqn3_path + 'dqn3_log.json'), 'r') as f:
            'dqn3_log.json should be inited as []'
            jlist = json.load(f)
        jlist.append(log_dict)
        with open((dqn3_path + 'dqn3_log.json'), 'w') as f:
            json.dump(jlist, f)
        del jlist
