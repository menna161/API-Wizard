from os import path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..repository.github_repository_manager import GithubRepositoryManager
from ..base.base_github_manager import BaseGithubManager
from ..constants import WINDOWS, PYTHON, NODE, DOTNET, POWERSHELL
from ..exceptions import LanguageNotSupportException


def _overwrite_yaml_file(self, data):
    sha = self._github_repo_mgr.get_content(self._github_repository, 'azure-pipelines.yml', get_metadata=True).get('sha')
    return self._github_repo_mgr.commit_file(repository_fullname=self._github_repository, file_path='azure-pipelines.yml', file_data=data, commit_message='Overwritten azure-pipelines.yml by Azure CLI ({time})'.format(time=datetime.utcnow().strftime('%Y-%m-%d %X UTC')), sha=sha)
