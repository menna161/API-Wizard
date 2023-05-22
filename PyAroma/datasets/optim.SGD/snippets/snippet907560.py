import itertools
import math
from abc import ABC, abstractmethod
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from tqdm.auto import tqdm
import logging
import variational
from torch.utils.data import DataLoader, Dataset
from torch.optim.optimizer import Optimizer
from utils import AverageMeter, get_error, get_device


def _fit_classifier(self, optimizer='adam', learning_rate=0.0004, weight_decay=0.0001, epochs=10):
    'Fits the last layer of the network using the cached features.'
    logging.info('Fitting final classifier...')
    if (not hasattr(self.model.classifier, 'input_features')):
        raise ValueError('You need to run `cache_features` on model before running `fit_classifier`')
    targets = self.model.classifier.targets.to(self.device)
    features = self.model.classifier.input_features.to(self.device)
    dataset = torch.utils.data.TensorDataset(features, targets)
    data_loader = _get_loader(dataset, **self.loader_opts)
    if (optimizer == 'adam'):
        optimizer = torch.optim.Adam(self.model.fc.parameters(), lr=learning_rate, weight_decay=weight_decay)
    elif (optimizer == 'sgd'):
        optimizer = torch.optim.SGD(self.model.fc.parameters(), lr=learning_rate, weight_decay=weight_decay)
    else:
        raise ValueError(f'Unsupported optimizer {optimizer}')
    loss_fn = nn.CrossEntropyLoss()
    for epoch in tqdm(range(epochs), desc='Fitting classifier', leave=False):
        metrics = AverageMeter()
        for (data, target) in data_loader:
            optimizer.zero_grad()
            output = self.model.classifier(data)
            loss = loss_fn(self.model.classifier(data), target)
            error = get_error(output, target)
            loss.backward()
            optimizer.step()
            metrics.update(n=data.size(0), loss=loss.item(), error=error)
        logging.info((f'[epoch {epoch}]: ' + '\t'.join((f'{k}: {v}' for (k, v) in metrics.avg.items()))))
