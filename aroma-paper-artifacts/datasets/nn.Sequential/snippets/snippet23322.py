import argparse
import os
import numpy as np
import pandas as pd
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from pytorch_pretrained_bert import BertModel
from torchvision import transforms
from torch.optim import RMSprop
from utils.text_process import process_dataframe
from utils.models import ImageTextDataset, Towers, return_adj_matrix
from utils.util import get_encoding, classification_loss_fn, graph_loss_fn, gap_loss_fn


def train(args):
    device = torch.device(('cuda:0' if args.cuda else 'cpu'))
    original_dataframe = pd.read_csv(args.csv_file_path)
    processed_dataframe = process_dataframe(original_dataframe)
    adj_matrix = return_adj_matrix(processed_dataframe)
    X = processed_dataframe.loc[(:, ['image', 'processed_text'])].values
    y = processed_dataframe['mapped_classes'].values
    transform = transforms.Compose([transforms.RandomRotation(5), transforms.RandomResizedCrop(284, scale=(0.9, 1.0)), transforms.ColorJitter(brightness=0.2, contrast=0.1, hue=0.07), transforms.ToTensor(), transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])
    trainset = ImageTextDataset(X, y, transform)
    trainloader = torch.utils.data.DataLoader(trainset, shuffle=True, batch_size=args.batch_size, drop_last=True)
    resnet50 = models.resnet50(pretrained=True).to(device)
    resnet50 = torch.nn.Sequential(*list(resnet50.children())[:(- 1)]).to(device)
    bert = BertModel.from_pretrained('bert-base-uncased').to(device)
    for param in resnet50.parameters():
        param.requires_grad = False
    for param in bert.parameters():
        param.requires_grad = False
    model = Towers(len(np.unique(y))).to(device)
    opt = RMSprop(model.parameters(), lr=args.lr, momentum=0.9)
    for e in range(args.epochs):
        loss_agg = 0
        classification_loss_agg = 0
        graph_loss_agg = 0
        gap_loss_agg = 0
        for (batch_id, data) in enumerate(trainloader):
            (imgs, texts, labels) = data
            imgs = imgs.to(device)
            labels = labels.to(device)
            img_embeddings = resnet50(imgs).to(device).squeeze(2).squeeze(2)
            text_embeddings = torch.stack([get_encoding(text, bert, device) for text in texts]).to(device)
            opt.zero_grad()
            (outputs, imgs_f, texts_f) = model(img_embeddings, text_embeddings)
            classification_loss = classification_loss_fn(outputs, labels)
            graph_loss = graph_loss_fn(outputs, labels, adj_matrix, device)
            gap_loss = gap_loss_fn(imgs_f, texts_f)
            loss = (((classification_loss * args.classification_weight) + (graph_loss * args.graph_weight)) + (gap_loss * args.gap_weight))
            loss_agg += loss.item()
            classification_loss_agg += classification_loss.item()
            graph_loss_agg += graph_loss.item()
            gap_loss_agg += gap_loss.item()
            loss.backward()
            opt.step()
            if (((batch_id + 1) % args.log_interval) == 0):
                mesg = '\tEpoch {}:  [{}/{}]\tloss: {:.6f}\tclf_avg_loss: {:.6f}\tgraph_avg_loss: {:.6f}\tgap_av_loss: {:.6f}\tloss_avg: {:.6f}'.format((e + 1), (args.batch_size * (batch_id + 1)), len(trainset), loss.item(), (classification_loss_agg / (batch_id + 1)), (graph_loss_agg / (batch_id + 1)), (gap_loss_agg / (batch_id + 1)), (loss_agg / (batch_id + 1)))
                print(mesg)
        if ((args.checkpoint_model_dir is not None) and os.path.exists(args.checkpoint_model_dir)):
            model.eval().cpu()
            ckpt_model_path = os.path.join(args.checkpoint_model_dir, 'checkpoint.pth.tar')
            torch.save({'epoch': (e + 1), 'network_state_dict': model.state_dict(), 'optimizer': opt.state_dict()}, ckpt_model_path)
            model.to(device).train()
    if ((args.save_model_dir is not None) and os.path.exists(args.save_model_dir)):
        model.eval().cpu()
        save_model_filename = (((('epoch_' + str(args.epochs)) + '_') + str(args.batch_size)) + '.pth.tar')
        save_model_path = os.path.join(args.save_model_dir, save_model_filename)
        torch.save(model.state_dict(), save_model_path)
        print('\nDone, trained model saved at', save_model_path)
