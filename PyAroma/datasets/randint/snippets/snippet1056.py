import numpy as np
from copy import deepcopy
import gc
import time
import logging
from Node.WU_UCTnode import WU_UCTnode
from Env.EnvWrapper import EnvWrapper
from ParallelPool.PoolManager import PoolManager
from Mem.CheckpointManager import CheckpointManager


def simulate_single_step(self, sim_idx):
    curr_node = self.root_node
    curr_depth = 1
    while True:
        if (curr_node.no_child_available() or ((not curr_node.all_child_visited()) and (curr_node != self.root_node) and (np.random.random() < 0.5)) or ((not curr_node.all_child_visited()) and (curr_node == self.root_node))):
            cloned_curr_node = curr_node.shallow_clone()
            checkpoint_data = self.checkpoint_data_manager.retrieve(curr_node.checkpoint_idx)
            self.expansion_task_recorder[sim_idx] = (checkpoint_data, cloned_curr_node, curr_node)
            self.unscheduled_expansion_tasks.append(sim_idx)
            need_expansion = True
            break
        else:
            action = curr_node.select_action()
        curr_node.update_history(sim_idx, action, curr_node.rewards[action])
        if (curr_node.dones[action] or (curr_depth >= self.max_depth)):
            need_expansion = False
            break
        if (curr_node.children[action] is None):
            need_expansion = False
            break
        next_node = curr_node.children[action]
        curr_depth += 1
        curr_node = next_node
    if (not need_expansion):
        if (not curr_node.dones[action]):
            self.simulation_task_recorder[sim_idx] = (action, curr_node, curr_node.checkpoint_idx, None)
            self.unscheduled_simulation_tasks.append(sim_idx)
        else:
            self.incomplete_update(curr_node, self.root_node, sim_idx)
            self.complete_update(curr_node, self.root_node, 0.0, sim_idx)
            self.simulation_count += 1
    else:
        while ((len(self.unscheduled_expansion_tasks) > 0) and self.expansion_worker_pool.has_idle_server()):
            curr_idx = np.random.randint(0, len(self.unscheduled_expansion_tasks))
            task_idx = self.unscheduled_expansion_tasks.pop(curr_idx)
            (checkpoint_data, cloned_curr_node, _) = self.expansion_task_recorder[task_idx]
            self.expansion_worker_pool.assign_expansion_task(checkpoint_data, cloned_curr_node, self.global_saving_idx, task_idx)
            self.global_saving_idx += 1
        if (self.expansion_worker_pool.server_occupied_rate() >= 0.99):
            (expand_action, next_state, reward, done, checkpoint_data, saving_idx, task_idx) = self.expansion_worker_pool.get_complete_expansion_task()
            curr_node = self.expansion_task_recorder.pop(task_idx)[2]
            curr_node.update_history(task_idx, expand_action, reward)
            curr_node.dones[expand_action] = done
            curr_node.rewards[expand_action] = reward
            if done:
                self.incomplete_update(curr_node, self.root_node, task_idx)
                self.complete_update(curr_node, self.root_node, 0.0, task_idx)
                self.simulation_count += 1
            else:
                self.checkpoint_data_manager.store(saving_idx, checkpoint_data)
                self.simulation_task_recorder[task_idx] = (expand_action, curr_node, saving_idx, deepcopy(next_state))
                self.unscheduled_simulation_tasks.append(task_idx)
    while ((len(self.unscheduled_simulation_tasks) > 0) and self.simulation_worker_pool.has_idle_server()):
        idx = np.random.randint(0, len(self.unscheduled_simulation_tasks))
        task_idx = self.unscheduled_simulation_tasks.pop(idx)
        checkpoint_data = self.checkpoint_data_manager.retrieve(self.simulation_task_recorder[task_idx][2])
        first_aciton = (None if (self.simulation_task_recorder[task_idx][3] is not None) else self.simulation_task_recorder[task_idx][0])
        self.simulation_worker_pool.assign_simulation_task(task_idx, checkpoint_data, first_action=first_aciton)
        self.incomplete_update(self.simulation_task_recorder[task_idx][1], self.root_node, task_idx)
    if (self.simulation_worker_pool.server_occupied_rate() >= 0.99):
        args = self.simulation_worker_pool.get_complete_simulation_task()
        if (len(args) == 3):
            (task_idx, accu_reward, prior_prob) = args
        else:
            (task_idx, accu_reward, reward, done) = args
        (expand_action, curr_node, saving_idx, next_state) = self.simulation_task_recorder.pop(task_idx)
        if (len(args) == 4):
            curr_node.rewards[expand_action] = reward
            curr_node.dones[expand_action] = done
        if (next_state is not None):
            curr_node.add_child(expand_action, next_state, saving_idx, prior_prob=prior_prob)
        self.complete_update(curr_node, self.root_node, accu_reward, task_idx)
        self.simulation_count += 1
