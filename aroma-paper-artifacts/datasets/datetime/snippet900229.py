import argparse
import os
from datetime import datetime
from os.path import join as pjoin
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from tensorboardX import SummaryWriter
from torch.utils import data
from tqdm import tqdm
import core.loss
import torchvision.utils as vutils
from core.augmentations import Compose, RandomHorizontallyFlip, RandomRotate, AddNoise
from core.loader.data_loader import *
from core.metrics import runningScore
from core.models import get_model
from core.utils import np_to_tb


def train(args):
    device = torch.device(('cuda' if torch.cuda.is_available() else 'cpu'))
    split_train_val(args, per_val=args.per_val)
    current_time = datetime.now().strftime('%b%d_%H%M%S')
    log_dir = os.path.join('runs', (current_time + '_{}'.format(args.arch)))
    writer = SummaryWriter(log_dir=log_dir)
    if args.aug:
        data_aug = Compose([RandomRotate(10), RandomHorizontallyFlip(), AddNoise()])
    else:
        data_aug = None
    train_set = section_loader(is_transform=True, split='train', augmentations=data_aug)
    val_set = section_loader(is_transform=True, split='val')
    n_classes = train_set.n_classes
    shuffle = False
    with open(pjoin('data', 'splits', 'section_train.txt'), 'r') as f:
        train_list = f.read().splitlines()
    with open(pjoin('data', 'splits', 'section_val.txt'), 'r') as f:
        val_list = f.read().splitlines()

    class CustomSamplerTrain(torch.utils.data.Sampler):

        def __iter__(self):
            char = [('i' if (np.random.randint(2) == 1) else 'x')]
            self.indices = [idx for (idx, name) in enumerate(train_list) if (char[0] in name)]
            return (self.indices[i] for i in torch.randperm(len(self.indices)))

    class CustomSamplerVal(torch.utils.data.Sampler):

        def __iter__(self):
            char = [('i' if (np.random.randint(2) == 1) else 'x')]
            self.indices = [idx for (idx, name) in enumerate(val_list) if (char[0] in name)]
            return (self.indices[i] for i in torch.randperm(len(self.indices)))
    trainloader = data.DataLoader(train_set, batch_size=args.batch_size, sampler=CustomSamplerTrain(train_list), num_workers=4, shuffle=shuffle)
    valloader = data.DataLoader(val_set, batch_size=args.batch_size, sampler=CustomSamplerVal(val_list), num_workers=4)
    running_metrics = runningScore(n_classes)
    running_metrics_val = runningScore(n_classes)
    if (args.resume is not None):
        if os.path.isfile(args.resume):
            print("Loading model and optimizer from checkpoint '{}'".format(args.resume))
            model = torch.load(args.resume)
        else:
            print("No checkpoint found at '{}'".format(args.resume))
    else:
        model = get_model(args.arch, args.pretrained, n_classes)
    model = torch.nn.DataParallel(model, device_ids=range(torch.cuda.device_count()))
    model = model.to(device)
    if hasattr(model.module, 'optimizer'):
        print('Using custom optimizer')
        optimizer = model.module.optimizer
    else:
        optimizer = torch.optim.Adam(model.parameters(), amsgrad=True)
    loss_fn = core.loss.cross_entropy
    if args.class_weights:
        class_weights = torch.tensor([0.7151, 0.8811, 0.5156, 0.9346, 0.9683, 0.9852], device=device, requires_grad=False)
    else:
        class_weights = None
    best_iou = (- 100.0)
    class_names = ['upper_ns', 'middle_ns', 'lower_ns', 'rijnland_chalk', 'scruff', 'zechstein']
    for arg in vars(args):
        text = ((arg + ': ') + str(getattr(args, arg)))
        writer.add_text('Parameters/', text)
    for epoch in range(args.n_epoch):
        model.train()
        (loss_train, total_iteration) = (0, 0)
        for (i, (images, labels)) in enumerate(trainloader):
            (image_original, labels_original) = (images, labels)
            (images, labels) = (images.to(device), labels.to(device))
            optimizer.zero_grad()
            outputs = model(images)
            pred = outputs.detach().max(1)[1].cpu().numpy()
            gt = labels.detach().cpu().numpy()
            running_metrics.update(gt, pred)
            loss = loss_fn(input=outputs, target=labels, weight=class_weights)
            loss_train += loss.item()
            loss.backward()
            if (args.clip != 0):
                torch.nn.utils.clip_grad_norm(model.parameters(), args.clip)
            optimizer.step()
            total_iteration = (total_iteration + 1)
            if ((i % 20) == 0):
                print(('Epoch [%d/%d] training Loss: %.4f' % ((epoch + 1), args.n_epoch, loss.item())))
            numbers = [0]
            if (i in numbers):
                tb_original_image = vutils.make_grid(image_original[0][0], normalize=True, scale_each=True)
                writer.add_image('train/original_image', tb_original_image, (epoch + 1))
                labels_original = labels_original.numpy()[0]
                correct_label_decoded = train_set.decode_segmap(np.squeeze(labels_original))
                writer.add_image('train/original_label', np_to_tb(correct_label_decoded), (epoch + 1))
                out = F.softmax(outputs, dim=1)
                prediction = out.max(1)[1].cpu().numpy()[0]
                confidence = out.max(1)[0].cpu().detach()[0]
                tb_confidence = vutils.make_grid(confidence, normalize=True, scale_each=True)
                decoded = train_set.decode_segmap(np.squeeze(prediction))
                writer.add_image('train/predicted', np_to_tb(decoded), (epoch + 1))
                writer.add_image('train/confidence', tb_confidence, (epoch + 1))
                unary = outputs.cpu().detach()
                unary_max = torch.max(unary)
                unary_min = torch.min(unary)
                unary = unary.add(((- 1) * unary_min))
                unary = (unary / (unary_max - unary_min))
                for channel in range(0, len(class_names)):
                    decoded_channel = unary[0][channel]
                    tb_channel = vutils.make_grid(decoded_channel, normalize=True, scale_each=True)
                    writer.add_image(f'train_classes/_{class_names[channel]}', tb_channel, (epoch + 1))
        loss_train /= total_iteration
        (score, class_iou) = running_metrics.get_scores()
        writer.add_scalar('train/Pixel Acc', score['Pixel Acc: '], (epoch + 1))
        writer.add_scalar('train/Mean Class Acc', score['Mean Class Acc: '], (epoch + 1))
        writer.add_scalar('train/Freq Weighted IoU', score['Freq Weighted IoU: '], (epoch + 1))
        writer.add_scalar('train/Mean_IoU', score['Mean IoU: '], (epoch + 1))
        running_metrics.reset()
        writer.add_scalar('train/loss', loss_train, (epoch + 1))
        if (args.per_val != 0):
            with torch.no_grad():
                model.eval()
                (loss_val, total_iteration_val) = (0, 0)
                for (i_val, (images_val, labels_val)) in tqdm(enumerate(valloader)):
                    (image_original, labels_original) = (images_val, labels_val)
                    (images_val, labels_val) = (images_val.to(device), labels_val.to(device))
                    outputs_val = model(images_val)
                    pred = outputs_val.detach().max(1)[1].cpu().numpy()
                    gt = labels_val.detach().cpu().numpy()
                    running_metrics_val.update(gt, pred)
                    loss = loss_fn(input=outputs_val, target=labels_val)
                    total_iteration_val = (total_iteration_val + 1)
                    if ((i_val % 20) == 0):
                        print(('Epoch [%d/%d] validation Loss: %.4f' % (epoch, args.n_epoch, loss.item())))
                    numbers = [0]
                    if (i_val in numbers):
                        tb_original_image = vutils.make_grid(image_original[0][0], normalize=True, scale_each=True)
                        writer.add_image('val/original_image', tb_original_image, epoch)
                        labels_original = labels_original.numpy()[0]
                        correct_label_decoded = train_set.decode_segmap(np.squeeze(labels_original))
                        writer.add_image('val/original_label', np_to_tb(correct_label_decoded), (epoch + 1))
                        out = F.softmax(outputs_val, dim=1)
                        prediction = out.max(1)[1].cpu().detach().numpy()[0]
                        confidence = out.max(1)[0].cpu().detach()[0]
                        tb_confidence = vutils.make_grid(confidence, normalize=True, scale_each=True)
                        decoded = train_set.decode_segmap(np.squeeze(prediction))
                        writer.add_image('val/predicted', np_to_tb(decoded), (epoch + 1))
                        writer.add_image('val/confidence', tb_confidence, (epoch + 1))
                        unary = outputs.cpu().detach()
                        (unary_max, unary_min) = (torch.max(unary), torch.min(unary))
                        unary = unary.add(((- 1) * unary_min))
                        unary = (unary / (unary_max - unary_min))
                        for channel in range(0, len(class_names)):
                            tb_channel = vutils.make_grid(unary[0][channel], normalize=True, scale_each=True)
                            writer.add_image(f'val_classes/_{class_names[channel]}', tb_channel, (epoch + 1))
                (score, class_iou) = running_metrics_val.get_scores()
                for (k, v) in score.items():
                    print(k, v)
                writer.add_scalar('val/Pixel Acc', score['Pixel Acc: '], (epoch + 1))
                writer.add_scalar('val/Mean IoU', score['Mean IoU: '], (epoch + 1))
                writer.add_scalar('val/Mean Class Acc', score['Mean Class Acc: '], (epoch + 1))
                writer.add_scalar('val/Freq Weighted IoU', score['Freq Weighted IoU: '], (epoch + 1))
                writer.add_scalar('val/loss', loss.item(), (epoch + 1))
                running_metrics_val.reset()
                if (score['Mean IoU: '] >= best_iou):
                    best_iou = score['Mean IoU: ']
                    model_dir = os.path.join(log_dir, f'{args.arch}_model.pkl')
                    torch.save(model, model_dir)
        elif (((epoch + 1) % 10) == 0):
            model_dir = os.path.join(log_dir, f'{args.arch}_ep{(epoch + 1)}_model.pkl')
            torch.save(model, model_dir)
    writer.close()
