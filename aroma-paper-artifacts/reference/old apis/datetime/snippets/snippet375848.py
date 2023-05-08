import os, time, logging
import zipfile, glob
import datetime
from typing import List, Mapping
import pandas as pd
from pandas import DataFrame
import tempfile
import bisect
from collections import namedtuple
from retry import retry
from kaggle.rest import ApiException
from kaggle.api.kaggle_api_extended import KaggleApi
from kaggle.models.kaggle_models_extended import File
from autogluon_utils.utils import *
from autogluon_utils.configs.kaggle.kaggle_competitions import KAGGLE_COMPETITIONS, CONFIG, eval_metric_lower_is_better
from autogluon_utils.configs.kaggle.constants import *
from autogluon_utils.configs.kaggle.common import *


@retry(exceptions=ApiException, tries=5, delay=10, backoff=5)
def submit_kaggle_competition(competition: str, submission_file: str) -> SubmissionResult:
    'Main wrapper for submitting a competition to kaggle with retries and get scores.\n    It will do retries when facing errors, eventually returns SubmissionResult or throws\n\n    :param competition: kaggle competition identifier\n    :param submission_file: path to the submission file\n\n    :raises: ScoreNotAvailable, kaggle.rest.ApiException\n    :return: instance of SubmissionResult\n    :rtype: SubmissionResult\n    '
    assert os.path.exists(submission_file)
    api = kaggle_api()
    timestamp = datetime.datetime.utcnow().timestamp()
    description = f'ts: {int(timestamp)}'
    api.competition_submit(submission_file, description, competition)
    time.sleep(30)
    submission_result = competition_score(competition, description)
    if ((not submission_result.error_description) and submission_result.public_score):
        lb_rank = leaderboard_rank(competition, submission_result.public_score)
        submission_result = submission_result._replace(leaderboard_rank=lb_rank.rank, num_teams=lb_rank.num_teams)
    return submission_result
