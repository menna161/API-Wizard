import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
import numpy as np
import pickle
from tqdm import tqdm
import time


def run_network(data, input_size, output_size, problem_type, net_kw, run_kw, num_workers=8, pin_memory=True, validate=True, val_patience=np.inf, test=False, ensemble=False, numepochs=100, wt_init=nn.init.kaiming_normal_, bias_init=(lambda x: nn.init.constant_(x, 0.1)), verbose=True):
    "\n    ARGS:\n        data:\n            6-ary tuple (xtr,ytr, xva,yva, xte,yte) from get_data_mlp(), OR\n            Dict with keys 'train', 'val', 'test' from get_data_cnn()\n        input_size, output_size, net_kw : See Net()\n        run_kw:\n            lr: Initial learning rate\n            gamma: Learning rate decay coefficient\n            milestones: When to step decay learning rate, e.g. 0.5 will decay lr halfway through training\n            weight_decay: Default 0\n            batch_size: Default 256\n        num_workers, pin_memory: Only required if using Pytorch data loaders\n            Generally, set num_workers equal to number of threads (e.g. my Macbook pro has 4 cores x 2 = 8 threads)\n        validate: Whether to do validation at the end of every epoch.\n        val_patience: If best val acc doesn't increase for this many epochs, then stop training. Set as np.inf to never stop training (until numepochs)\n        test: True - Test at end, False - don't\n        ensemble: If True, return feedforward soft outputs to be later used for ensembling\n        numepochs: Self explanatory\n        wt_init, bias_init: Respective pytorch functions\n        verbose: Print messages\n    \n    RETURNS:\n        net: Complete net\n        recs: Dictionary with a key for each stat collected and corresponding value for all values of the stat\n    "
    net = Net(input_size=input_size, output_size=output_size, **net_kw)
    if (torch.cuda.device_count() > 1):
        print('Using {0} GPUs'.format(torch.cuda.device_count()))
        net = nn.DataParallel(net)
    net.to(device)
    for i in range(len(net.mlp)):
        if (wt_init is not None):
            wt_init(net.mlp[i].weight.data)
        if (bias_init is not None):
            bias_init(net.mlp[i].bias.data)
    lr = (run_kw['lr'] if ('lr' in run_kw) else run_kws_defaults['lr'])
    gamma = (run_kw['gamma'] if ('gamma' in run_kw) else run_kws_defaults['gamma'])
    milestones = (run_kw['milestones'] if ('milestones' in run_kw) else run_kws_defaults['milestones'])
    weight_decay = (run_kw['weight_decay'] if ('weight_decay' in run_kw) else run_kws_defaults['weight_decay'])
    batch_size = (run_kw['batch_size'] if ('batch_size' in run_kw) else run_kws_defaults['batch_size'])
    if (not isinstance(batch_size, int)):
        batch_size = batch_size.item()
    if (problem_type == 'classification'):
        lossfunc = nn.CrossEntropyLoss(reduction='mean')
    elif (problem_type == 'regression'):
        lossfunc = nn.MSELoss()
    opt = torch.optim.Adam(net.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(opt, milestones=[int((numepochs * milestone)) for milestone in milestones], gamma=gamma)
    if (type(data) == dict):
        loader = True
        train_loader = torch.utils.data.DataLoader(data['train'], batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=pin_memory)
        if (validate is True):
            val_loader = torch.utils.data.DataLoader(data['val'], batch_size=len(data['val']), num_workers=num_workers, pin_memory=pin_memory)
        if (test is True):
            test_loader = torch.utils.data.DataLoader(data['test'], batch_size=len(data['test']), num_workers=num_workers, pin_memory=pin_memory)
    else:
        loader = False
        (xtr, ytr, xva, yva, xte, yte) = data
    recs = {'train_accs': np.zeros(numepochs), 'train_losses': np.zeros(numepochs), 'val_accs': (np.zeros(numepochs) if (validate is True) else None), 'val_losses': (np.zeros(numepochs) if (validate is True) else None), 'val_final_outputs': (numepochs * [0])}
    total_t = 0
    best_val_acc = (- np.inf)
    best_val_loss = np.inf
    for epoch in range(numepochs):
        if verbose:
            print('Epoch {0}'.format((epoch + 1)))
        numbatches = (int(np.ceil((xtr.shape[0] / batch_size))) if (not loader) else len(train_loader))
        if (not loader):
            shuff = torch.randperm(xtr.shape[0])
            (xtr, ytr) = (xtr[shuff], ytr[shuff])
        epoch_correct = 0
        epoch_loss = 0.0
        t = time.time()
        net.train()
        for batch in tqdm((range(numbatches) if (not loader) else train_loader), leave=False):
            if (not loader):
                inputs = xtr[(batch * batch_size):((batch + 1) * batch_size)]
                labels = ytr[(batch * batch_size):((batch + 1) * batch_size)]
            else:
                (inputs, labels) = batch
                (inputs, labels) = (inputs.to(device), labels.to(device))
            (batch_correct, batch_loss) = train_batch(x=inputs, y=labels, net=net, lossfunc=lossfunc, opt=opt)
            epoch_correct += batch_correct
            epoch_loss += batch_loss
        t_epoch = (time.time() - t)
        if ((epoch > 0) or (numepochs == 1)):
            total_t += t_epoch
        recs['train_accs'][epoch] = (((100 * epoch_correct) / xtr.shape[0]) if (not loader) else ((100 * epoch_correct) / len(data['train'])))
        recs['train_losses'][epoch] = (epoch_loss / numbatches)
        if verbose:
            print('Training Acc = {0}%, Loss = {1}'.format(np.round(recs['train_accs'][epoch], 2), np.round(recs['train_losses'][epoch], 3)))
        if (validate is True):
            if (not loader):
                (correct, loss, _, final_outputs) = eval_data(net=net, x=xva, ensemble=ensemble, y=yva, lossfunc=lossfunc)
                recs['val_accs'][epoch] = ((100 * correct) / xva.shape[0])
                recs['val_losses'][epoch] = loss
            else:
                epoch_correct = 0
                epoch_loss = 0.0
                for batch in tqdm(val_loader, leave=False):
                    (inputs, labels) = batch
                    (inputs, labels) = (inputs.to(device), labels.to(device))
                    (batch_correct, batch_loss, _, final_outputs) = eval_data(net=net, x=inputs, ensemble=ensemble, y=labels, lossfunc=lossfunc)
                    epoch_correct += batch_correct
                    epoch_loss += batch_loss
                val_acc = ((100 * epoch_correct) / len(data['val']))
                val_loss = (epoch_loss / len(val_loader))
                recs['val_accs'][epoch] = val_acc
                recs['val_losses'][epoch] = val_loss
            recs['val_final_outputs'][epoch] = final_outputs
            if verbose:
                print('Validation Acc = {0}%, Loss = {1}'.format(np.round(recs['val_accs'][epoch], 2), np.round(recs['val_losses'][epoch], 3)))
            if (problem_type == 'classification'):
                if (recs['val_accs'][epoch] > best_val_acc):
                    best_val_acc = recs['val_accs'][epoch]
                    best_val_ep = (epoch + 1)
                    val_patience_counter = 0
                else:
                    val_patience_counter += 1
                    if (val_patience_counter == val_patience):
                        print('Early stopped after epoch {0}'.format((epoch + 1)))
                        numepochs = (epoch + 1)
                        break
            elif (problem_type == 'regression'):
                if (recs['val_losses'][epoch] < best_val_loss):
                    best_val_loss = recs['val_losses'][epoch]
                    best_val_ep = (epoch + 1)
                    val_patience_counter = 0
                else:
                    val_patience_counter += 1
                    if (val_patience_counter == val_patience):
                        print('Early stopped after epoch {0}'.format((epoch + 1)))
                        numepochs = (epoch + 1)
                        break
        scheduler.step()
    if (validate is True):
        if (problem_type == 'classification'):
            print('\nBest validation accuracy = {0}% obtained in epoch {1}'.format(best_val_acc, best_val_ep))
        elif (problem_type == 'regression'):
            print('\nBest validation loss = {0} obtained in epoch {1}'.format(best_val_loss, best_val_ep))
    if (test is True):
        if (not loader):
            (correct, loss, _, final_outputs) = eval_data(net=net, x=xte, ensemble=ensemble, y=yte, lossfunc=lossfunc)
            recs['test_acc'] = ((100 * correct) / xte.shape[0])
            recs['test_loss'] = loss
        else:
            overall_correct = 0
            overall_loss = 0.0
            for batch in tqdm(test_loader, leave=False):
                (inputs, labels) = batch
                (inputs, labels) = (inputs.to(device), labels.to(device))
                (batch_correct, batch_loss, _, final_outputs) = eval_data(net=net, x=inputs, ensemble=ensemble, y=labels, lossfunc=lossfunc)
                overall_correct += batch_correct
                overall_loss += batch_loss
            recs['test_acc'] = ((100 * overall_correct) / len(data['test']))
            recs['test_loss'] = (overall_loss / len(test_loader))
        recs['test_final_outputs'] = final_outputs
        print('Test accuracy = {0}%, Loss = {1}\n'.format(np.round(recs['test_acc'], 2), np.round(recs['test_loss'], 3)))
    recs['t_epoch'] = ((total_t / (numepochs - 1)) if (numepochs > 1) else total_t)
    print('Avg time taken per epoch = {0}'.format(recs['t_epoch']))
    recs = {**{key: recs[key][:numepochs] for key in recs if hasattr(recs[key], '__iter__')}, **{key: recs[key] for key in recs if (not hasattr(recs[key], '__iter__'))}}
    return (net, recs)
