from alpha_net_c4 import ConnectNet, AlphaLoss, board_data
import os
import pickle
import datetime
import numpy as np
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.nn.utils import clip_grad_norm_
import matplotlib.pyplot as plt
import logging


def train(net, dataset, optimizer, scheduler, start_epoch, cpu, args, iteration):
    torch.manual_seed(cpu)
    cuda = torch.cuda.is_available()
    net.train()
    criterion = AlphaLoss()
    train_set = board_data(dataset)
    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, num_workers=0, pin_memory=False)
    losses_per_epoch = load_results((iteration + 1))
    logger.info('Starting training process...')
    update_size = (len(train_loader) // 10)
    print(('Update step size: %d' % update_size))
    for epoch in range(start_epoch, args.num_epochs):
        total_loss = 0.0
        losses_per_batch = []
        for (i, data) in enumerate(train_loader, 0):
            (state, policy, value) = data
            (state, policy, value) = (state.float(), policy.float(), value.float())
            if cuda:
                (state, policy, value) = (state.cuda(), policy.cuda(), value.cuda())
            (policy_pred, value_pred) = net(state)
            loss = criterion(value_pred[:, 0], value, policy_pred, policy)
            loss = (loss / args.gradient_acc_steps)
            loss.backward()
            clip_grad_norm_(net.parameters(), args.max_norm)
            if ((epoch % args.gradient_acc_steps) == 0):
                optimizer.step()
                optimizer.zero_grad()
            total_loss += loss.item()
            if ((i % update_size) == (update_size - 1)):
                losses_per_batch.append(((args.gradient_acc_steps * total_loss) / update_size))
                print(('[Iteration %d] Process ID: %d [Epoch: %d, %5d/ %d points] total loss per batch: %.3f' % (iteration, os.getpid(), (epoch + 1), ((i + 1) * args.batch_size), len(train_set), losses_per_batch[(- 1)])))
                print('Policy (actual, predicted):', policy[0].argmax().item(), policy_pred[0].argmax().item())
                print('Policy data:', policy[0])
                print('Policy pred:', policy_pred[0])
                print('Value (actual, predicted):', value[0].item(), value_pred[(0, 0)].item())
                print(' ')
                total_loss = 0.0
        scheduler.step()
        if (len(losses_per_batch) >= 1):
            losses_per_epoch.append((sum(losses_per_batch) / len(losses_per_batch)))
        if ((epoch % 2) == 0):
            save_as_pickle(('losses_per_epoch_iter%d.pkl' % (iteration + 1)), losses_per_epoch)
            torch.save({'epoch': (epoch + 1), 'state_dict': net.state_dict(), 'optimizer': optimizer.state_dict(), 'scheduler': scheduler.state_dict()}, os.path.join('./model_data/', ('%s_iter%d.pth.tar' % (args.neural_net_name, (iteration + 1)))))
        '\n        # Early stopping\n        if len(losses_per_epoch) > 50:\n            if abs(sum(losses_per_epoch[-4:-1])/3-sum(losses_per_epoch[-16:-13])/3) <= 0.00017:\n                break\n        '
    logger.info('Finished Training!')
    fig = plt.figure()
    ax = fig.add_subplot(222)
    ax.scatter([e for e in range(start_epoch, (len(losses_per_epoch) + start_epoch))], losses_per_epoch)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss per batch')
    ax.set_title('Loss vs Epoch')
    plt.savefig(os.path.join('./model_data/', ('Loss_vs_Epoch_iter%d_%s.png' % ((iteration + 1), datetime.datetime.today().strftime('%Y-%m-%d')))))
    plt.show()
