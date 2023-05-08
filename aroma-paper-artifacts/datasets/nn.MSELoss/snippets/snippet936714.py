from model import rec_model
from dataset import MovieRankDataset
from torch.utils.data import DataLoader
import torch
import torch.optim as optim
import torch.nn as nn
from tensorboardX import SummaryWriter
from recInterface import saveMovieAndUserFeature


def train(model, num_epochs=5, lr=0.0001):
    loss_function = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    datasets = MovieRankDataset(pkl_file='data.p')
    dataloader = DataLoader(datasets, batch_size=256, shuffle=True)
    losses = []
    writer = SummaryWriter()
    for epoch in range(num_epochs):
        loss_all = 0
        for (i_batch, sample_batch) in enumerate(dataloader):
            user_inputs = sample_batch['user_inputs']
            movie_inputs = sample_batch['movie_inputs']
            target = sample_batch['target'].to(device)
            model.zero_grad()
            (tag_rank, _, _) = model(user_inputs, movie_inputs)
            loss = loss_function(tag_rank, target)
            if ((i_batch % 20) == 0):
                writer.add_scalar('data/loss', loss, (i_batch * 20))
                print(loss)
            loss_all += loss
            loss.backward()
            optimizer.step()
        print('Epoch {}:\t loss:{}'.format(epoch, loss_all))
    writer.export_scalars_to_json('./test.json')
    writer.close()
