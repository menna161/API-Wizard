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


def add_datarun(self, dataset_id, budget=100, budget_type='classifier', gridding=0, k_window=3, metric='f1', methods=['logreg', 'dt', 'knn'], r_minimum=2, run_per_partition=False, score_target='cv', priority=1, selector='uniform', tuner='uniform', deadline=None):
    "Register one or more Dataruns to the Database.\n\n        The methods hyperparameters will be analyzed and Hyperpartitions generated\n        from them.\n        If ``run_per_partition`` is ``True``, one Datarun will be created for each\n        Hyperpartition. Otherwise, a single one will be created for all of them.\n\n        Args:\n            dataset_id (int):\n                Id of the Dataset which this Datarun will belong to.\n            budget (int):\n                Budget amount. Optional. Defaults to ``100``.\n            budget_type (str):\n                Budget Type. Can be 'classifier' or 'walltime'.\n                Optional. Defaults to ``'classifier'``.\n            gridding (int):\n                ``gridding`` setting for the Tuner. Optional. Defaults to ``0``.\n            k_window (int):\n                ``k`` setting for the Selector. Optional. Defaults to ``3``.\n            metric (str):\n                Metric to use for the tuning and selection. Optional. Defaults to ``'f1'``.\n            methods (list):\n                List of methods to try. Optional. Defaults to ``['logreg', 'dt', 'knn']``.\n            r_minimum (int):\n                ``r_minimum`` setting for the Tuner. Optional. Defaults to ``2``.\n            run_per_partition (bool):\n                whether to create a separated Datarun for each Hyperpartition or not.\n                Optional. Defaults to ``False``.\n            score_target (str):\n                Which score to use for the tuning and selection process. It can be ``'cv'`` or\n                ``'test'``. Optional. Defaults to ``'cv'``.\n            priority (int):\n                Priority of this Datarun. The higher the better. Optional. Defaults to ``1``.\n            selector (str):\n                Type of selector to use. Optional. Defaults to ``'uniform'``.\n            tuner (str):\n                Type of tuner to use. Optional. Defaults to ``'uniform'``.\n            deadline (str):\n                Time deadline. It must be a string representing a datetime in the format\n                ``'%Y-%m-%d %H:%M'``. If given, ``budget_type`` will be set to ``'walltime'``.\n\n        Returns:\n            Datarun:\n                The created Datarun or list of Dataruns.\n        "
    if deadline:
        deadline = datetime.strptime(deadline, TIME_FMT)
        budget_type = 'walltime'
    elif (budget_type == 'walltime'):
        deadline = (datetime.now() + timedelta(minutes=budget))
    run_description = '___'.join([tuner, selector])
    target = (score_target + '_judgment_metric')
    method_parts = {}
    for method in methods:
        method_instance = Method(method)
        method_parts[method] = method_instance.get_hyperpartitions()
        LOGGER.info('method {} has {} hyperpartitions'.format(method, len(method_parts[method])))
    dataruns = list()
    if (not run_per_partition):
        datarun = self.db.create_datarun(dataset_id=dataset_id, description=run_description, tuner=tuner, selector=selector, gridding=gridding, priority=priority, budget_type=budget_type, budget=budget, deadline=deadline, metric=metric, score_target=target, k_window=k_window, r_minimum=r_minimum)
        dataruns.append(datarun)
    for (method, parts) in method_parts.items():
        for part in parts:
            if run_per_partition:
                datarun = self.db.create_datarun(dataset_id=dataset_id, description=run_description, tuner=tuner, selector=selector, gridding=gridding, priority=priority, budget_type=budget_type, budget=budget, deadline=deadline, metric=metric, score_target=target, k_window=k_window, r_minimum=r_minimum)
                dataruns.append(datarun)
            self.db.create_hyperpartition(datarun_id=datarun.id, method=method, tunables=part.tunables, constants=part.constants, categoricals=part.categoricals, status=PartitionStatus.INCOMPLETE)
    dataset = self.db.get_dataset(dataset_id)
    LOGGER.info('Dataruns created. Summary:')
    LOGGER.info('\tDataset ID: {}'.format(dataset.id))
    LOGGER.info('\tTraining data: {}'.format(dataset.train_path))
    LOGGER.info('\tTest data: {}'.format(dataset.test_path))
    if run_per_partition:
        LOGGER.info('\tDatarun IDs: {}'.format(', '.join((str(datarun.id) for datarun in dataruns))))
    else:
        LOGGER.info('\tDatarun ID: {}'.format(dataruns[0].id))
    LOGGER.info('\tHyperpartition selection strategy: {}'.format(dataruns[0].selector))
    LOGGER.info('\tParameter tuning strategy: {}'.format(dataruns[0].tuner))
    LOGGER.info('\tBudget: {} ({})'.format(dataruns[0].budget, dataruns[0].budget_type))
    return (dataruns if run_per_partition else dataruns[0])
