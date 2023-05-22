import torch
from torchvision import transforms
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, PackedSequence
from model import ModelSpatioTemporal
from dataset import VideoAttTarget_video
from config import *
from lib.pytorch_convolutional_rnn import convolutional_rnn
import argparse
import os
from datetime import datetime
import shutil
import numpy as np
import warnings


def train():
    transform = _get_transform()
    print('Loading Data')
    train_dataset = VideoAttTarget_video(videoattentiontarget_train_data, videoattentiontarget_train_label, transform=transform, test=False, seq_len_limit=50)
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0, collate_fn=video_pack_sequences)
    logdir = os.path.join(args.log_dir, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    if os.path.exists(logdir):
        shutil.rmtree(logdir)
    os.makedirs(logdir)
    np.random.seed(1)
    device = torch.device('cuda', args.device)
    num_lstm_layers = 2
    print('Constructing model')
    model = ModelSpatioTemporal(num_lstm_layers=num_lstm_layers)
    model.cuda(device)
    if args.init_weights:
        print('Loading weights')
        model_dict = model.state_dict()
        snapshot = torch.load(args.init_weights)
        snapshot = snapshot['model']
        model_dict.update(snapshot)
        model.load_state_dict(model_dict)
    mse_loss = nn.MSELoss(reduce=False)
    bcelogit_loss = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam([{'params': model.convlstm_scene.parameters(), 'lr': args.lr}, {'params': model.deconv1.parameters(), 'lr': args.lr}, {'params': model.deconv2.parameters(), 'lr': args.lr}, {'params': model.deconv3.parameters(), 'lr': args.lr}, {'params': model.conv4.parameters(), 'lr': args.lr}, {'params': model.fc_inout.parameters(), 'lr': (args.lr * 5)}], lr=0)
    step = 0
    loss_amp_factor = 10000
    max_steps = len(train_loader)
    optimizer.zero_grad()
    print('Training in progress ...')
    for ep in range(args.epochs):
        for (batch, (img, face, head_channel, gaze_heatmap, inout_label, lengths)) in enumerate(train_loader):
            model.train(True)
            for module in model.modules():
                if isinstance(module, torch.nn.modules.BatchNorm1d):
                    module.eval()
                if isinstance(module, torch.nn.modules.BatchNorm2d):
                    module.eval()
                if isinstance(module, torch.nn.modules.BatchNorm3d):
                    module.eval()
            (X_pad_data_img, X_pad_sizes) = pack_padded_sequence(img, lengths, batch_first=True)
            (X_pad_data_head, _) = pack_padded_sequence(head_channel, lengths, batch_first=True)
            (X_pad_data_face, _) = pack_padded_sequence(face, lengths, batch_first=True)
            (Y_pad_data_heatmap, _) = pack_padded_sequence(gaze_heatmap, lengths, batch_first=True)
            (Y_pad_data_inout, _) = pack_padded_sequence(inout_label, lengths, batch_first=True)
            hx = (torch.zeros((num_lstm_layers, args.batch_size, 512, 7, 7)).cuda(device), torch.zeros((num_lstm_layers, args.batch_size, 512, 7, 7)).cuda(device))
            last_index = 0
            previous_hx_size = args.batch_size
            for i in range(0, lengths[0], args.chunk_size):
                X_pad_sizes_slice = X_pad_sizes[i:(i + args.chunk_size)].cuda(device)
                curr_length = np.sum(X_pad_sizes_slice.cpu().detach().numpy())
                X_pad_data_slice_img = X_pad_data_img[last_index:(last_index + curr_length)].cuda(device)
                X_pad_data_slice_head = X_pad_data_head[last_index:(last_index + curr_length)].cuda(device)
                X_pad_data_slice_face = X_pad_data_face[last_index:(last_index + curr_length)].cuda(device)
                Y_pad_data_slice_heatmap = Y_pad_data_heatmap[last_index:(last_index + curr_length)].cuda(device)
                Y_pad_data_slice_inout = Y_pad_data_inout[last_index:(last_index + curr_length)].cuda(device)
                last_index += curr_length
                prev_hx = (hx[0][(:, :min(X_pad_sizes_slice[0], previous_hx_size), :, :, :)].detach(), hx[1][(:, :min(X_pad_sizes_slice[0], previous_hx_size), :, :, :)].detach())
                (deconv, inout_val, hx) = model(X_pad_data_slice_img, X_pad_data_slice_head, X_pad_data_slice_face, hidden_scene=prev_hx, batch_sizes=X_pad_sizes_slice)
                l2_loss = (mse_loss(deconv.squeeze(1), Y_pad_data_slice_heatmap) * loss_amp_factor)
                l2_loss = torch.mean(l2_loss, dim=1)
                l2_loss = torch.mean(l2_loss, dim=1)
                Y_pad_data_slice_inout = Y_pad_data_slice_inout.cuda(device).to(torch.float).squeeze()
                l2_loss = torch.mul(l2_loss, Y_pad_data_slice_inout)
                l2_loss = (torch.sum(l2_loss) / torch.sum(Y_pad_data_slice_inout))
                Xent_loss = (bcelogit_loss(inout_val.squeeze(), Y_pad_data_slice_inout.squeeze()) * 100)
                total_loss = (l2_loss + Xent_loss)
                total_loss.backward()
                optimizer.step()
                optimizer.zero_grad()
                previous_hx_size = X_pad_sizes_slice[(- 1)]
                step += 1
        if ((ep % args.save_every) == 0):
            checkpoint = {'model': model.state_dict()}
            torch.save(checkpoint, os.path.join(logdir, ('epoch_%02d_weights.pt' % (ep + 1))))
