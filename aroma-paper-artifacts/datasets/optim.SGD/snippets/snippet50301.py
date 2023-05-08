from random import randint
import numpy as np
from os.path import join, dirname, abspath
import sys
import argparse
from evidence_inference.preprocess.preprocessor import SimpleInferenceVectorizer as SimpleInferenceVectorizer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
import torch
from torch import optim
import torch.nn as nn
from torch.nn import functional as F
from torch.autograd import Variable
from torch.nn.utils.rnn import pad_sequence
from evidence_inference.models.model_0 import InferenceNet, GRUEncoder, _get_y_vec, PaddedSequence
from evidence_inference.models.model_scan import sample_train, train_reformat, scan_reform, early_stopping
import pdb
import pdb


def train_scan(inference_vectorizer, train_Xy, val_Xy, test_Xy, epochs=1, batch_size=1, patience=3):
    scan_net = ScanNet(inference_vectorizer)
    if USE_CUDA:
        scan_net = scan_net.cuda()
    optimizer = torch.optim.SGD(scan_net.parameters(), lr=0.01)
    criterion = nn.BCELoss(reduction='sum')
    bow = Bag_of_words(inference_vectorizer)
    total_epoch_loss = []
    for epoch in range(epochs):
        if early_stopping(total_epoch_loss, patience):
            break
        epoch_loss = 0
        epoch_samples = sample_train(train_Xy)
        for i in range(0, len(epoch_samples), batch_size):
            instances = epoch_samples[i:(i + batch_size)]
            ys = torch.FloatTensor([inst['y'] for inst in instances])
            sens = torch.FloatTensor([bow.transform(inst['sentence_span']) for inst in instances])
            optimizer.zero_grad()
            if USE_CUDA:
                sens = sens.cuda()
                ys = ys.cuda()
            tags = scan_net(sens)
            loss = criterion(tags, ys)
            if (loss.item() != loss.item()):
                import pdb
                pdb.set_trace()
            epoch_loss += loss.item()
            loss.backward()
            optimizer.step()
        with torch.no_grad():
            instances = val_Xy
            y_hat = []
            val_loss = 0
            y_true = [inst['y'] for inst in val_Xy]
            for i in range(0, len(instances), batch_size):
                batch_instances = instances[i:(i + batch_size)]
                sens = torch.FloatTensor([bow.transform(inst['sentence_span']) for inst in batch_instances])
                ys = torch.FloatTensor([inst['y'] for inst in batch_instances])
                if USE_CUDA:
                    sens = sens.cuda()
                    ys = ys.cuda()
                tags = scan_net(sens, batch_size=len(batch_instances))
                val_loss += criterion(tags, ys)
                y_hat = np.append(y_hat, tags.data.cpu().numpy())
            y_hat = [(1 if (y > 0.5) else 0) for y in y_hat]
            acc = accuracy_score(y_true, y_hat)
            f1 = f1_score(y_true, y_hat)
            prc = precision_score(y_true, y_hat)
            rc = recall_score(y_true, y_hat)
            print('epoch {}. train loss: {:.2f}; val loss: {:.2f}; val acc: {:.2f}; val f1: {:.2f}; val precision: {:.2f}; val recall: {:.2f}'.format(epoch, epoch_loss, val_loss, acc, f1, prc, rc))
            total_epoch_loss.append(val_loss)
    return scan_net
