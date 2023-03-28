from environments.list_env import ListEnv, ListEnvEncoder
from core.curriculum import CurriculumScheduler
from core.policy import Policy
import core.config as conf
from core.trainer import Trainer
from core.prioritized_replay_buffer import PrioritizedReplayBuffer
import argparse
import numpy as np
import torch
from tensorboardX import SummaryWriter
import time

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', help='random seed', default=1, type=int)
    parser.add_argument('--tensorboard', help='display on tensorboard', action='store_true')
    parser.add_argument('--verbose', help='print training monitoring in console', action='store_true')
    parser.add_argument('--save-model', help='save neural network model', action='store_true')
    parser.add_argument('--save-results', help='save training progress in .txt file', action='store_true')
    parser.add_argument('--num-cpus', help='number of cpus to use', default=8, type=int)
    args = parser.parse_args()
    seed = args.seed
    tensorboard = args.tensorboard
    verbose = args.verbose
    save_model = args.save_model
    save_results = args.save_results
    num_cpus = args.num_cpus
    torch.set_num_threads(num_cpus)
    ts = time.localtime(time.time())
    date_time = '{}_{}_{}-{}_{}_{}'.format(ts[0], ts[1], ts[2], ts[3], ts[4], ts[5])
    model_save_path = '../models/list_npi_{}-{}.pth'.format(date_time, seed)
    results_save_path = '../results/list_npi_{}-{}.txt'.format(date_time, seed)
    tensorboard_path = 'runs/list_npi_{}-{}'.format(date_time, seed)
    if tensorboard:
        writer = SummaryWriter(tensorboard_path)
    if save_results:
        results_file = open(results_save_path, 'w')
    np.random.seed(seed)
    torch.manual_seed(seed)
    env_tmp = ListEnv(length=5, encoding_dim=conf.encoding_dim)
    num_programs = env_tmp.get_num_programs()
    num_non_primary_programs = env_tmp.get_num_non_primary_programs()
    observation_dim = env_tmp.get_observation_dim()
    programs_library = env_tmp.programs_library
    encoder = ListEnvEncoder(env_tmp.get_observation_dim(), conf.encoding_dim)
    indices_non_primary_programs = [p['index'] for (_, p) in programs_library.items() if (p['level'] > 0)]
    policy = Policy(encoder, conf.hidden_size, num_programs, num_non_primary_programs, conf.program_embedding_dim, conf.encoding_dim, indices_non_primary_programs, conf.learning_rate)
    idx_tasks = [prog['index'] for (key, prog) in env_tmp.programs_library.items() if (prog['level'] > 0)]
    buffer = PrioritizedReplayBuffer(conf.buffer_max_length, idx_tasks, p1=conf.proba_replay_buffer)
    curriculum_scheduler = CurriculumScheduler(conf.reward_threshold, num_non_primary_programs, programs_library, moving_average=0.99)
    length = 5
    max_depth_dict = {1: 5, 2: ((2 * length) + 3), 3: ((2 * length) + 3)}
    mcts_train_params = {'number_of_simulations': conf.number_of_simulations, 'max_depth_dict': max_depth_dict, 'temperature': conf.temperature, 'c_puct': conf.c_puct, 'exploit': False, 'level_closeness_coeff': conf.level_closeness_coeff, 'gamma': conf.gamma, 'use_dirichlet_noise': True}
    mcts_test_params = {'number_of_simulations': conf.number_of_simulations_for_validation, 'max_depth_dict': max_depth_dict, 'temperature': conf.temperature, 'c_puct': conf.c_puct, 'exploit': True, 'level_closeness_coeff': conf.level_closeness_coeff, 'gamma': conf.gamma}
    trainer = Trainer(env_tmp, policy, buffer, curriculum_scheduler, mcts_train_params, mcts_test_params, conf.num_validation_episodes, conf.num_episodes_per_task, conf.batch_size, conf.num_updates_per_episode, verbose)
    min_length = 2
    max_length = 7
    validation_length = 7
    for iteration in range(conf.num_iterations):
        task_index = curriculum_scheduler.get_next_task_index()
        task_level = env_tmp.get_program_level_from_index(task_index)
        length = np.random.randint(min_length, (max_length + 1))
        env = ListEnv(length=length, encoding_dim=conf.encoding_dim)
        max_depth_dict = {1: 5, 2: ((2 * length) + 3), 3: ((2 * length) + 3)}
        trainer.env = env
        trainer.mcts_train_params['max_depth_dict'] = max_depth_dict
        trainer.mcts_test_params['max_depth_dict'] = max_depth_dict
        trainer.play_iteration(task_index)
        if verbose:
            print('Start validation .....')
        for idx in curriculum_scheduler.get_tasks_of_maximum_level():
            task_level = env_tmp.get_program_level_from_index(idx)
            length = validation_length
            env = ListEnv(length=length, encoding_dim=conf.encoding_dim)
            max_depth_dict = {1: 5, 2: ((2 * length) + 3), 3: ((2 * length) + 3)}
            trainer.env = env
            trainer.mcts_train_params['max_depth_dict'] = max_depth_dict
            trainer.mcts_test_params['max_depth_dict'] = max_depth_dict
            (v_rewards, v_lengths, programs_failed_indices) = trainer.perform_validation_step(idx)
            curriculum_scheduler.update_statistics(idx, v_rewards)
        if tensorboard:
            for idx in curriculum_scheduler.get_tasks_of_maximum_level():
                v_task_name = env.get_program_from_index(idx)
                writer.add_scalar(('validation/' + v_task_name), curriculum_scheduler.get_statistic(idx), iteration)
        if save_results:
            str = 'Iteration: {}'.format(iteration)
            for idx in curriculum_scheduler.indices_non_primary_programs:
                task_name = env.get_program_from_index(idx)
                str += (', %s:%.3f' % (task_name, curriculum_scheduler.get_statistic(idx)))
            str += '\n'
            results_file.write(str)
        if verbose:
            curriculum_scheduler.print_statistics()
            print('')
            print('')
        if (curriculum_scheduler.maximum_level > env.get_maximum_level()):
            break
        if save_model:
            torch.save(policy.state_dict(), model_save_path)
    if verbose:
        print('End of training !')
    if tensorboard:
        writer.close()
    if save_results:
        results_file.close()
