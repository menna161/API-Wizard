import torch
import numpy as np
from importlib import import_module
from .default import NormalNN
from .regularization import SI, L2, EWC, MAS
from dataloaders.wrapper import Storage


def learn_batch(self, train_loader, val_loader=None):
    if self.skip_memory_concatenation:
        new_train_loader = train_loader
    else:
        dataset_list = []
        for storage in self.task_memory.values():
            dataset_list.append(storage)
        dataset_list *= max((len(train_loader.dataset) // self.memory_size), 1)
        dataset_list.append(train_loader.dataset)
        dataset = torch.utils.data.ConcatDataset(dataset_list)
        new_train_loader = torch.utils.data.DataLoader(dataset, batch_size=train_loader.batch_size, shuffle=True, num_workers=train_loader.num_workers)
    super(Naive_Rehearsal, self).learn_batch(new_train_loader, val_loader)
    self.task_count += 1
    num_sample_per_task = (self.memory_size // self.task_count)
    num_sample_per_task = min(len(train_loader.dataset), num_sample_per_task)
    for storage in self.task_memory.values():
        storage.reduce(num_sample_per_task)
    randind = torch.randperm(len(train_loader.dataset))[:num_sample_per_task]
    self.task_memory[self.task_count] = Storage(train_loader.dataset, randind)
