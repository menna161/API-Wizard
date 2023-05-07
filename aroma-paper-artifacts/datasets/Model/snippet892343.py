import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import TensorDataset, DataLoader
import argparse
import os

if (__name__ == '__main__'):
    num_classes = 28
    num_epochs = 300
    batch_size = 2048
    input_size = 1
    model_dir = 'model'
    log = 'Adam_batch_size={}_epoch={}'.format(str(batch_size), str(num_epochs))
    parser = argparse.ArgumentParser()
    parser.add_argument('-num_layers', default=2, type=int)
    parser.add_argument('-hidden_size', default=64, type=int)
    parser.add_argument('-window_size', default=10, type=int)
    args = parser.parse_args()
    num_layers = args.num_layers
    hidden_size = args.hidden_size
    window_size = args.window_size
    model = Model(input_size, hidden_size, num_layers, num_classes).to(device)
    seq_dataset = generate('hdfs_train')
    dataloader = DataLoader(seq_dataset, batch_size=batch_size, shuffle=True, pin_memory=True)
    writer = SummaryWriter(log_dir=('log/' + log))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())
    start_time = time.time()
    total_step = len(dataloader)
    for epoch in range(num_epochs):
        train_loss = 0
        for (step, (seq, label)) in enumerate(dataloader):
            seq = seq.clone().detach().view((- 1), window_size, input_size).to(device)
            output = model(seq)
            loss = criterion(output, label.to(device))
            optimizer.zero_grad()
            loss.backward()
            train_loss += loss.item()
            optimizer.step()
            writer.add_graph(model, seq)
        print('Epoch [{}/{}], train_loss: {:.4f}'.format((epoch + 1), num_epochs, (train_loss / total_step)))
        writer.add_scalar('train_loss', (train_loss / total_step), (epoch + 1))
    elapsed_time = (time.time() - start_time)
    print('elapsed_time: {:.3f}s'.format(elapsed_time))
    if (not os.path.isdir(model_dir)):
        os.makedirs(model_dir)
    torch.save(model.state_dict(), (((model_dir + '/') + log) + '.pt'))
    writer.close()
    print('Finished Training')
