import numpy as np
from torchvision.datasets import CIFAR10, CIFAR100
from .dataset import ClassificationTaskDataset
from .expansion import ClassificationTaskExpander


def generate(self, task_id=0, transform=None, target_transform=None):
    'Generate tasks given the classes\n\n        Parameters\n        ----------\n        task_id : int 0-10 (default 0)\n            0 = CIFAR10, 1 = first 10 of CIFAR100, 2 = second 10 of CIFAR100, ...\n        transform : callable (default None)\n            Optional transform to be applied on a sample.\n        target_transform : callable (default None)\n            Optional transform to be applied on a label.\n\n        Returns\n        -------\n        Task\n        '
    assert isinstance(task_id, int)
    assert (0 <= task_id <= 10), task_id
    task_expander = ClassificationTaskExpander()
    if (task_id == 0):
        classes = tuple(range(10))
        return task_expander(self.cifar10_dataset, {c: new_c for (new_c, c) in enumerate(classes)}, label_names={c: name for (c, name) in self.cifar10_dataset.label_names_map.items()}, task_id=task_id, task_name='Split CIFAR: CIFAR-10 {}'.format(classes), transform=transform, target_transform=target_transform)
    else:
        classes = tuple([int(c) for c in (np.arange(10) + (10 * (task_id - 1)))])
        return task_expander(self.cifar100_dataset, {c: new_c for (new_c, c) in enumerate(classes)}, label_names={classes.index(old_c): name for (old_c, name) in self.cifar100_dataset.label_names_map.items() if (old_c in classes)}, task_id=task_id, task_name='Split CIFAR: CIFAR-100 {}'.format(classes), transform=transform, target_transform=target_transform)
