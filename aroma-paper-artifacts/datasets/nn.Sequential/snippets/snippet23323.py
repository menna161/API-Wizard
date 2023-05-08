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


def evaluate(args):
    device = torch.device(('cuda:0' if args.cuda else 'cpu'))
    dataframe = pd.read_csv(args.csv_file_path)
    processed_dataframe = process_dataframe(dataframe)
    X = processed_dataframe.loc[(:, ['image', 'processed_text'])].values
    y = processed_dataframe['mapped_classes'].values
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])
    valset = ImageTextDataset(X, y, transform)
    valloader = torch.utils.data.DataLoader(valset, shuffle=False, batch_size=1)
    resnet50 = models.resnet50(pretrained=True).to(device)
    resnet50 = torch.nn.Sequential(*list(resnet50.children())[:(- 1)]).to(device).eval()
    bert = BertModel.from_pretrained('bert-base-uncased').to(device).eval()
    model = Towers().to(device).eval()
    model.load_state_dict(torch.load(args.model))
    correct = 0
    val_loss = 0
    pred_label_pairs = []
    with torch.no_grad():
        for data in valloader:
            (img, text, label) = data
            img = img.to(device)
            label = label.to(device)
            img_embeddings = resnet50(img).to(device).squeeze(2).squeeze(2)
            text_embeddings = torch.stack([get_encoding(text, bert, device) for text in text]).to(device)
            (pred, img_f, text_f) = model(img_embeddings, text_embeddings)
            classification_loss = classification_loss_fn(pred, label)
            gap_loss = gap_loss_fn(img_f, text_f)
            loss = (classification_loss + gap_loss)
            val_loss += loss.item()
            pred = pred.data.max(1)[1]
            correct += pred.eq(label.data).sum().item()
            pred_label_pairs.append((label.item(), pred.item()))
        val_loss /= len(valloader.dataset)
        val_accuracy = ((100.0 * correct) / len(valloader.dataset))
        pd.DataFrame(pred_label_pairs, columns=['label', 'predicted']).to_csv('predictions.csv', header=True, index=False)
        return ((('Loss: ' + str(val_loss)) + ', Accuracy: ') + str(val_accuracy))
