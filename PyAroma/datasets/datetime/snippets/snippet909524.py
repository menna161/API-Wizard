import torch
import numpy as np
import copy
import datetime


def _train(model, epochs, criterion, optimizer, dataloader, test_loader, device, lr_scheduler):
    val_acc_history = []
    train_acc_history = []
    loss_train_history = []
    loss_val_history = []
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    for epoch in range(epochs):
        print('Epoch {}/{}'.format((epoch + 1), epochs))
        print(('-' * 30))
        if (lr_scheduler is not None):
            for param_group in optimizer.param_groups:
                print('Learning Rate: {}'.format(param_group['lr']))
            print(('-' * 30))
        for phase in ['train', 'validation']:
            if (phase == 'train'):
                model.train()
            else:
                model.eval()
            running_loss = 0
            running_corrects = 0
            total = 0
            for (inputs, labels) in dataloader[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)
                optimizer.zero_grad()
                with torch.set_grad_enabled((phase == 'train')):
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    (_, preds) = torch.max(outputs, 1)
                    if (phase == 'train'):
                        loss.backward()
                        optimizer.step()
                running_loss += (loss.item() * inputs.size(0))
                running_corrects += (preds == labels).sum().item()
                total += labels.size(0)
            epoch_loss = (running_loss / total)
            epoch_acc = (running_corrects / total)
            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))
            import datetime
            print(datetime.datetime.now())
            if (phase == 'train'):
                train_acc_history.append(epoch_acc)
                loss_train_history.append(epoch_loss)
            if (phase == 'validation'):
                val_acc_history.append(epoch_acc)
                loss_val_history.append(epoch_loss)
                if (lr_scheduler is not None):
                    if (lr_scheduler.__class__.__name__ == 'ReduceLROnPlateau'):
                        lr_scheduler.step(epoch_acc)
            if ((phase == 'validation') and (epoch_acc > best_acc)):
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
                print('Test accuracy:')
                test(model, test_loader, device)
        print()
    print('Best Val Acc: {:.4f}'.format(best_acc))
    model.load_state_dict(best_model_wts)
    return (model, val_acc_history, loss_val_history, train_acc_history, loss_train_history)
