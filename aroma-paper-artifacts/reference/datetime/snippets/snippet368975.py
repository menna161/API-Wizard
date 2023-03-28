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


def work(self, datarun_ids=None, save_files=True, choose_randomly=True, cloud_mode=False, total_time=None, wait=True, verbose=False):
    'Get unfinished Dataruns from the database and work on them.\n\n        Check the ModelHub Database for unfinished Dataruns, and work on them\n        as they are added. This process will continue to run until it exceeds\n        total_time or there are no more Dataruns to process or it is killed.\n\n        Args:\n            datarun_ids (list):\n                list of IDs of Dataruns to work on. If ``None``, this will work on any\n                unfinished Dataruns found in the database. Optional. Defaults to ``None``.\n            save_files (bool):\n                Whether to save the fitted classifiers and their metrics or not.\n                Optional. Defaults to True.\n            choose_randomly (bool):\n                If ``True``, work on all the highest-priority dataruns in random order.\n                Otherwise, work on them in sequential order (by ID).\n                Optional. Defaults to ``True``.\n            cloud_mode (bool):\n                Save the models and metrics in AWS S3 instead of locally. This option\n                works only if S3 configuration has been provided on initialization.\n                Optional. Defaults to ``False``.\n            total_time (int):\n                Total time to run the work process, in seconds. If ``None``, continue to\n                run until interrupted or there are no more Dataruns to process.\n                Optional. Defaults to ``None``.\n            wait (bool):\n                If ``True``, wait for more Dataruns to be inserted into the Database\n                once all have been processed. Otherwise, exit the worker loop\n                when they run out.\n                Optional. Defaults to ``False``.\n            verbose (bool):\n                Whether to be verbose about the process. Optional. Defaults to ``True``.\n        '
    start_time = datetime.now()
    while True:
        dataruns = self.db.get_dataruns(include_ids=datarun_ids, ignore_complete=True)
        if (not dataruns):
            if wait:
                LOGGER.debug('No dataruns found. Sleeping %d seconds and trying again.', self._LOOP_WAIT)
                time.sleep(self._LOOP_WAIT)
                continue
            else:
                LOGGER.info('No dataruns found. Exiting.')
                break
        if choose_randomly:
            run = random.choice(dataruns)
        else:
            run = sorted(dataruns, key=attrgetter('id'))[0]
        self.db.mark_datarun_running(run.id)
        LOGGER.info(('Computing on datarun %d' % run.id))
        worker = Worker(self.db, run, save_files=save_files, cloud_mode=cloud_mode, aws_access_key=self.aws_access_key, aws_secret_key=self.aws_secret_key, s3_bucket=self.s3_bucket, s3_folder=self.s3_folder, models_dir=self.models_dir, metrics_dir=self.metrics_dir, verbose_metrics=self.verbose_metrics)
        try:
            if (run.budget_type == 'classifier'):
                pbar = tqdm(total=run.budget, ascii=True, initial=run.completed_classifiers, disable=(not verbose))
                while (run.status != RunStatus.COMPLETE):
                    worker.run_classifier()
                    run = self.db.get_datarun(run.id)
                    if (verbose and (run.completed_classifiers > pbar.last_print_n)):
                        pbar.update((run.completed_classifiers - pbar.last_print_n))
                pbar.close()
            elif (run.budget_type == 'walltime'):
                pbar = tqdm(disable=(not verbose), ascii=True, initial=run.completed_classifiers, unit=' Classifiers')
                while (run.status != RunStatus.COMPLETE):
                    worker.run_classifier()
                    run = self.db.get_datarun(run.id)
                    if (verbose and (run.completed_classifiers > pbar.last_print_n)):
                        pbar.update((run.completed_classifiers - pbar.last_print_n))
                pbar.close()
        except ClassifierError:
            LOGGER.error('Something went wrong. Sleeping %d seconds.', self._LOOP_WAIT)
            time.sleep(self._LOOP_WAIT)
        elapsed_time = (datetime.now() - start_time).total_seconds()
        if ((total_time is not None) and (elapsed_time >= total_time)):
            LOGGER.info('Total run time for worker exceeded; exiting.')
            break
