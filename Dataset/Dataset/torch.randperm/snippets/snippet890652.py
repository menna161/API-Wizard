import torch
from random import shuffle
from .wrapper import Subclass, AppendName, Permutation


def SplitGen(train_dataset, val_dataset, first_split_sz=2, other_split_sz=2, rand_split=False, remap_class=False):
    '\n    Generate the dataset splits based on the labels.\n    :param train_dataset: (torch.utils.data.dataset)\n    :param val_dataset: (torch.utils.data.dataset)\n    :param first_split_sz: (int)\n    :param other_split_sz: (int)\n    :param rand_split: (bool) Randomize the set of label in each split\n    :param remap_class: (bool) Ex: remap classes in a split from [2,4,6 ...] to [0,1,2 ...]\n    :return: train_loaders {task_name:loader}, val_loaders {task_name:loader}, out_dim {task_name:num_classes}\n    '
    assert (train_dataset.number_classes == val_dataset.number_classes), 'Train/Val has different number of classes'
    num_classes = train_dataset.number_classes
    split_boundaries = [0, first_split_sz]
    while (split_boundaries[(- 1)] < num_classes):
        split_boundaries.append((split_boundaries[(- 1)] + other_split_sz))
    print('split_boundaries:', split_boundaries)
    assert (split_boundaries[(- 1)] == num_classes), 'Invalid split size'
    if (not rand_split):
        class_lists = {str(i): list(range(split_boundaries[(i - 1)], split_boundaries[i])) for i in range(1, len(split_boundaries))}
    else:
        randseq = torch.randperm(num_classes)
        class_lists = {str(i): randseq[list(range(split_boundaries[(i - 1)], split_boundaries[i]))].tolist() for i in range(1, len(split_boundaries))}
    print(class_lists)
    train_dataset_splits = {}
    val_dataset_splits = {}
    task_output_space = {}
    for (name, class_list) in class_lists.items():
        train_dataset_splits[name] = AppendName(Subclass(train_dataset, class_list, remap_class), name)
        val_dataset_splits[name] = AppendName(Subclass(val_dataset, class_list, remap_class), name)
        task_output_space[name] = len(class_list)
    return (train_dataset_splits, val_dataset_splits, task_output_space)
