import torch
from torchvision import transforms
import torch.nn as nn
from model import ModelSpatial
from dataset import GazeFollow
from config import *
from utils import imutils, evaluation
import argparse
import os
from datetime import datetime
import shutil
import numpy as np
from scipy.misc import imresize
from tensorboardX import SummaryWriter
import warnings


def train():
    transform = _get_transform()
    print('Loading Data')
    train_dataset = GazeFollow(gazefollow_train_data, gazefollow_train_label, transform, input_size=input_resolution, output_size=output_resolution)
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_dataset = GazeFollow(gazefollow_val_data, gazefollow_val_label, transform, input_size=input_resolution, output_size=output_resolution, test=True)
    val_loader = torch.utils.data.DataLoader(dataset=val_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    logdir = os.path.join(args.log_dir, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    if os.path.exists(logdir):
        shutil.rmtree(logdir)
    os.makedirs(logdir)
    writer = SummaryWriter(logdir)
    np.random.seed(1)
    device = torch.device('cuda', args.device)
    print('Constructing model')
    model = ModelSpatial()
    model.cuda().to(device)
    if args.init_weights:
        model_dict = model.state_dict()
        pretrained_dict = torch.load(args.init_weights)
        pretrained_dict = pretrained_dict['model']
        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)
    mse_loss = nn.MSELoss(reduce=False)
    bcelogit_loss = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    step = 0
    loss_amp_factor = 10000
    max_steps = len(train_loader)
    optimizer.zero_grad()
    print('Training in progress ...')
    for ep in range(args.epochs):
        for (batch, (img, face, head_channel, gaze_heatmap, name, gaze_inside)) in enumerate(train_loader):
            model.train(True)
            images = img.cuda().to(device)
            head = head_channel.cuda().to(device)
            faces = face.cuda().to(device)
            gaze_heatmap = gaze_heatmap.cuda().to(device)
            (gaze_heatmap_pred, attmap, inout_pred) = model(images, head, faces)
            gaze_heatmap_pred = gaze_heatmap_pred.squeeze(1)
            l2_loss = (mse_loss(gaze_heatmap_pred, gaze_heatmap) * loss_amp_factor)
            l2_loss = torch.mean(l2_loss, dim=1)
            l2_loss = torch.mean(l2_loss, dim=1)
            gaze_inside = gaze_inside.cuda(device).to(torch.float)
            l2_loss = torch.mul(l2_loss, gaze_inside)
            l2_loss = (torch.sum(l2_loss) / torch.sum(gaze_inside))
            Xent_loss = (bcelogit_loss(inout_pred.squeeze(), gaze_inside.squeeze()) * 100)
            total_loss = l2_loss
            total_loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            step += 1
            if ((batch % args.print_every) == 0):
                print('Epoch:{:04d}\tstep:{:06d}/{:06d}\ttraining loss: (l2){:.4f} (Xent){:.4f}'.format(ep, (batch + 1), max_steps, l2_loss, Xent_loss))
                ind = np.random.choice(len(images), replace=False)
                writer.add_scalar('Train Loss', total_loss, global_step=step)
            if (((batch != 0) and ((batch % args.eval_every) == 0)) or ((batch + 1) == max_steps)):
                print('Validation in progress ...')
                model.train(False)
                AUC = []
                min_dist = []
                avg_dist = []
                with torch.no_grad():
                    for (val_batch, (val_img, val_face, val_head_channel, val_gaze_heatmap, cont_gaze, imsize, _)) in enumerate(val_loader):
                        val_images = val_img.cuda().to(device)
                        val_head = val_head_channel.cuda().to(device)
                        val_faces = val_face.cuda().to(device)
                        val_gaze_heatmap = val_gaze_heatmap.cuda().to(device)
                        (val_gaze_heatmap_pred, val_attmap, val_inout_pred) = model(val_images, val_head, val_faces)
                        val_gaze_heatmap_pred = val_gaze_heatmap_pred.squeeze(1)
                        for b_i in range(len(cont_gaze)):
                            valid_gaze = cont_gaze[b_i]
                            valid_gaze = valid_gaze[(valid_gaze != (- 1))].view((- 1), 2)
                            multi_hot = imutils.multi_hot_targets(cont_gaze[b_i], imsize[b_i])
                            scaled_heatmap = imresize(val_gaze_heatmap_pred[b_i], (imsize[b_i][1], imsize[b_i][0]), interp='bilinear')
                            auc_score = evaluation.auc(scaled_heatmap, multi_hot)
                            AUC.append(auc_score)
                            (pred_x, pred_y) = evaluation.argmax_pts(val_gaze_heatmap_pred[b_i])
                            norm_p = [(pred_x / float(output_resolution)), (pred_y / float(output_resolution))]
                            all_distances = []
                            for gt_gaze in valid_gaze:
                                all_distances.append(evaluation.L2_dist(gt_gaze, norm_p))
                            min_dist.append(min(all_distances))
                            mean_gt_gaze = torch.mean(valid_gaze, 0)
                            avg_distance = evaluation.L2_dist(mean_gt_gaze, norm_p)
                            avg_dist.append(avg_distance)
                print('\tAUC:{:.4f}\tmin dist:{:.4f}\tavg dist:{:.4f}'.format(torch.mean(torch.tensor(AUC)), torch.mean(torch.tensor(min_dist)), torch.mean(torch.tensor(avg_dist))))
                val_ind = np.random.choice(len(val_images), replace=False)
                writer.add_scalar('Validation AUC', torch.mean(torch.tensor(AUC)), global_step=step)
                writer.add_scalar('Validation min dist', torch.mean(torch.tensor(min_dist)), global_step=step)
                writer.add_scalar('Validation avg dist', torch.mean(torch.tensor(avg_dist)), global_step=step)
        if ((ep % args.save_every) == 0):
            checkpoint = {'model': model.state_dict()}
            torch.save(checkpoint, os.path.join(logdir, ('epoch_%02d_weights.pt' % (ep + 1))))
