import os.path as osp
import sys
from amazing_brick.game.wrapped_amazing_brick import GameState
from amazing_brick.game.amazing_brick_utils import CONST
from DQN_train.gym_wrapper import AmazingBrickEnv2
import tianshou as ts
import torch, numpy as np
from torch import nn
import torch.nn.functional as F
import json
import datetime

if (__name__ == '__main__'):
    round = 0
    try:
        policy.load_state_dict(torch.load((dqn2_path + 'dqn2.pth')))
        lines = []
        with open((dqn2_path + 'dqn2_log.json'), 'r') as f:
            for line in f.readlines():
                cur_dict = json.loads(line)
                lines.append(cur_dict)
        log_dict = lines[(- 1)]
        print(log_dict)
        round = log_dict['round']
        del lines
    except FileNotFoundError as identifier:
        print('\n\nWe shall train a bright new net.\n')
        pass
    while True:
        round += 1
        print('\n\nround:{}\n\n'.format(round))
        result = ts.trainer.offpolicy_trainer(policy, train_collector, test_collector, max_epoch=max_epoch, step_per_epoch=step_per_epoch, collect_per_step=collect_per_step, episode_per_test=30, batch_size=64, train_fn=(lambda e1, e2: policy.set_eps(((0.1 * (max_epoch - e1)) / round))), test_fn=(lambda e1, e2: policy.set_eps(((0.05 * (max_epoch - e1)) / round))), writer=None)
        print(f"Finished training! Use {result['duration']}")
        torch.save(policy.state_dict(), (dqn2_path + 'dqn2.pth'))
        policy.load_state_dict(torch.load((dqn2_path + 'dqn2.pth')))
        log_dict = {}
        log_dict['round'] = round
        log_dict['last_train_time'] = datetime.datetime.now().strftime('%y-%m-%d %I:%M:%S %p %a')
        log_dict['result'] = json.dumps(result)
        with open((dqn2_path + 'dqn2_log.json'), 'a+') as f:
            f.write('\n')
            json.dump(log_dict, f)
