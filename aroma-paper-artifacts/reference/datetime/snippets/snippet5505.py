import os
import time
from datetime import datetime
import gym
import torch
import csv
import pickle
from model import ActorCritic
from utils import state_to_tensor, plot_line


def test(rank, args, T, shared_model):
    torch.manual_seed((args.seed + rank))
    env = gym.make(args.env)
    env.seed((args.seed + rank))
    model = ActorCritic(env.observation_space, env.action_space, args.hidden_size)
    model.eval()
    save_dir = os.path.join('results', args.name)
    can_test = True
    t_start = 1
    (rewards, steps) = ([], [])
    l = str(len(str(args.T_max)))
    done = True
    results_dict = {'t': [], 'reward': [], 'avg_steps': [], 'time': []}
    while (T.value() <= args.T_max):
        if can_test:
            t_start = T.value()
            (avg_rewards, avg_episode_lengths) = ([], [])
            for _ in range(args.evaluation_episodes):
                while True:
                    if done:
                        model.load_state_dict(shared_model.state_dict())
                        hx = torch.zeros(1, args.hidden_size)
                        cx = torch.zeros(1, args.hidden_size)
                        state = state_to_tensor(env.reset())
                        (done, episode_length) = (False, 0)
                        reward_sum = 0
                    if args.render:
                        env.render()
                    with torch.no_grad():
                        (policy, _, _, (hx, cx)) = model(state, (hx, cx))
                    action = policy.max(1)[1][0]
                    (state, reward, done, _) = env.step(action.item())
                    state = state_to_tensor(state)
                    reward_sum += reward
                    done = (done or (episode_length >= args.max_episode_length))
                    episode_length += 1
                    if done:
                        avg_rewards.append(reward_sum)
                        avg_episode_lengths.append(episode_length)
                        break
            print((('[{}] Step: {:<' + l) + '} Avg. Reward: {:<8} Avg. Episode Length: {:<8}').format(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S,%f')[:(- 3)], t_start, (sum(avg_rewards) / args.evaluation_episodes), (sum(avg_episode_lengths) / args.evaluation_episodes)))
            fields = [t_start, (sum(avg_rewards) / args.evaluation_episodes), (sum(avg_episode_lengths) / args.evaluation_episodes), str(datetime.now())]
            results_dict['t'].append(t_start)
            results_dict['reward'].append((sum(avg_rewards) / args.evaluation_episodes))
            results_dict['avg_steps'].append((sum(avg_episode_lengths) / args.evaluation_episodes))
            results_dict['time'].append(str(datetime.now()))
            with open(os.path.join(save_dir, 'results.pck'), 'wb') as f:
                pickle.dump(results_dict, f)
            with open(os.path.join(save_dir, 'results.csv'), 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            if args.evaluate:
                return
            rewards.append(avg_rewards)
            steps.append(t_start)
            plot_line(steps, rewards, save_dir)
            torch.save(model.state_dict(), os.path.join(save_dir, 'model.pth'))
            can_test = False
        elif ((T.value() - t_start) >= args.evaluation_interval):
            can_test = True
        time.sleep(0.001)
    with open(os.path.join(save_dir, 'results.pck'), 'wb') as f:
        pickle.dump(results_dict, f)
    env.close()
