from os import path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..repository.github_repository_manager import GithubRepositoryManager
from ..base.base_github_manager import BaseGithubManager
from ..constants import WINDOWS, PYTHON, NODE, DOTNET, POWERSHELL
from ..exceptions import LanguageNotSupportException


def _commit_yaml_file(self, data):
    return self._github_repo_mgr.commit_file(repository_fullname=self._github_repository, file_path='azure-pipelines.yml', file_data=data, commit_message='Created azure-pipelines.yml by Azure CLI ({time})'.format(time=datetime.utcnow().strftime('%Y-%m-%d %X UTC')))
