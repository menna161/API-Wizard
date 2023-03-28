import copy
import csv
import datetime
import json
import logging
import os
import time
from typing import Dict
import git


def gather_metadata() -> Dict:
    date_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    try:
        import git
        try:
            repo = git.Repo(search_parent_directories=True)
            git_sha = repo.commit().hexsha
            git_data = dict(commit=git_sha, branch=(None if repo.head.is_detached else repo.active_branch.name), is_dirty=repo.is_dirty(), path=repo.git_dir)
        except git.InvalidGitRepositoryError:
            git_data = None
    except ImportError:
        git_data = None
    if ('SLURM_JOB_ID' in os.environ):
        slurm_env_keys = [k for k in os.environ if k.startswith('SLURM')]
        slurm_data = {}
        for k in slurm_env_keys:
            d_key = k.replace('SLURM_', '').replace('SLURMD_', '').lower()
            slurm_data[d_key] = os.environ[k]
    else:
        slurm_data = None
    return dict(date_start=date_start, date_end=None, successful=False, git=git_data, slurm=slurm_data, env=os.environ.copy())
