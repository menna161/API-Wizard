import logging
import random
import time
from datetime import datetime, timedelta
from operator import attrgetter
from tqdm import tqdm
from atm.constants import TIME_FMT, PartitionStatus, RunStatus
from atm.database import Database
from atm.method import Method
from atm.worker import ClassifierError, Worker


def run(self, train_path, test_path=None, name=None, description=None, class_column='class', budget=100, budget_type='classifier', gridding=0, k_window=3, metric='f1', methods=['logreg', 'dt', 'knn'], r_minimum=2, run_per_partition=False, score_target='cv', selector='uniform', tuner='uniform', deadline=None, priority=1, save_files=True, choose_randomly=True, cloud_mode=False, total_time=None, verbose=True):
    "Create a Dataset and a Datarun and then work on it.\n\n        Args:\n            train_path (str):\n                Path to the training CSV file. It can be a local filesystem path,\n                absolute or relative, or an HTTP or HTTPS URL, or an S3 path in the\n                format ``s3://{bucket_name}/{key}``. Required.\n            test_path (str):\n                Path to the testing CSV file. It can be a local filesystem path,\n                absolute or relative, or an HTTP or HTTPS URL, or an S3 path in the\n                format ``s3://{bucket_name}/{key}``.\n                Optional. If not given, the training CSV will be split in two parts,\n                train and test.\n            name (str):\n                Name given to this dataset. Optional. If not given, a hash will be\n                generated from the training_path and used as the Dataset name.\n            description (str):\n                Human friendly description of the Dataset. Optional.\n            class_column (str):\n                Name of the column that will be used as the target variable.\n                Optional. Defaults to ``'class'``.\n            budget (int):\n                Budget amount. Optional. Defaults to ``100``.\n            budget_type (str):\n                Budget Type. Can be 'classifier' or 'walltime'.\n                Optional. Defaults to ``'classifier'``.\n            gridding (int):\n                ``gridding`` setting for the Tuner. Optional. Defaults to ``0``.\n            k_window (int):\n                ``k`` setting for the Selector. Optional. Defaults to ``3``.\n            metric (str):\n                Metric to use for the tuning and selection. Optional. Defaults to ``'f1'``.\n            methods (list):\n                List of methods to try. Optional. Defaults to ``['logreg', 'dt', 'knn']``.\n            r_minimum (int):\n                ``r_minimum`` setting for the Tuner. Optional. Defaults to ``2``.\n            run_per_partition (bool):\n                whether to create a separated Datarun for each Hyperpartition or not.\n                Optional. Defaults to ``False``.\n            score_target (str):\n                Which score to use for the tuning and selection process. It can be ``'cv'`` or\n                ``'test'``. Optional. Defaults to ``'cv'``.\n            priority (int):\n                Priority of this Datarun. The higher the better. Optional. Defaults to ``1``.\n            selector (str):\n                Type of selector to use. Optional. Defaults to ``'uniform'``.\n            tuner (str):\n                Type of tuner to use. Optional. Defaults to ``'uniform'``.\n            deadline (str):\n                Time deadline. It must be a string representing a datetime in the format\n                ``'%Y-%m-%d %H:%M'``. If given, ``budget_type`` will be set to ``'walltime'``.\n            verbose (bool):\n                Whether to be verbose about the process. Optional. Defaults to ``True``.\n\n        Returns:\n            Datarun:\n                The created Datarun or list of Dataruns.\n        "
    dataset = self.add_dataset(train_path, test_path, name, description, class_column)
    datarun = self.add_datarun(dataset.id, budget, budget_type, gridding, k_window, metric, methods, r_minimum, run_per_partition, score_target, priority, selector, tuner, deadline)
    if run_per_partition:
        datarun_ids = [_datarun.id for _datarun in datarun]
    else:
        datarun_ids = [datarun.id]
    if verbose:
        print('Processing dataset {}'.format(train_path))
    self.work(datarun_ids, save_files, choose_randomly, cloud_mode, total_time, False, verbose=verbose)
    dataruns = self.db.get_dataruns(include_ids=datarun_ids, ignore_complete=False, ignore_pending=True)
    if run_per_partition:
        return dataruns
    elif (len(dataruns) == 1):
        return dataruns[0]
