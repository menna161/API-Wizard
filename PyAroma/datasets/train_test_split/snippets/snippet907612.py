import os
import csv
from .dataset import ClassificationTaskDataset
from .expansion import MetaclassClassificationTaskExpander


def __init__(self, root, split='train', classes_file=CLASSES_FILE, metadata={}, transform=None, target_transform=None):
    path = os.path.join(root, 'cub/CUB_200_2011')
    images_folder = os.path.join(path, CUBDataset.IMAGES_FOLDER)
    images_file = os.path.join(path, CUBDataset.IMAGES_FILE)
    train_test_split_file = os.path.join(path, CUBDataset.TRAIN_TEST_SPLIT_FILE)
    image_class_labels_file = os.path.join(path, CUBDataset.IMAGE_CLASS_LABELS_FILE)
    classes_file = os.path.join(path, classes_file)
    assert os.path.exists(images_folder), images_folder
    assert os.path.exists(images_file), images_file
    assert os.path.exists(image_class_labels_file), image_class_labels_file
    ignore_indices = set()
    if (split is not None):
        assert (split in CUBDataset.POSSIBLE_SPLITS), split
        assert os.path.exists(train_test_split_file), train_test_split_file
        with open(train_test_split_file, 'r') as f:
            for l in f:
                (index, is_train) = l.strip().split(' ')
                if (int(is_train) and (split == CUBDataset.TEST_SPLIT)):
                    ignore_indices.add(int(index))
                elif ((not int(is_train)) and (split == CUBDataset.TRAIN_SPLIT)):
                    ignore_indices.add(int(index))
    images_list = []
    with open(images_file, 'r') as f:
        for l in f:
            (index, img) = l.strip().split(' ')
            if (int(index) not in ignore_indices):
                images_list.append(os.path.join(CUBDataset.IMAGES_FOLDER, img))
    labels_list = []
    with open(image_class_labels_file, 'r') as f:
        for l in f:
            (index, label) = l.strip().split(' ')
            if (int(index) not in ignore_indices):
                labels_list.append(int(label))
    label_names = {}
    if os.path.exists(classes_file):
        with open(classes_file, 'r') as f:
            for l in f:
                (label, label_name) = l.strip().split(' ', 1)
                label_names[int(label)] = label_name
    self.split = split
    super(CUBDataset, self).__init__(images_list, labels_list, label_names=label_names, root=path, task_id=None, task_name='CUB', metadata=metadata, transform=transform, target_transform=target_transform)
