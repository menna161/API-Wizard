import datetime
import json
import logging
import os
import shutil
import subprocess
import sys
import typing
from dataclasses import dataclass
from pathlib import Path
import boto3
import yaml


def __post_init__(self) -> None:
    self.logger = get_logger()
    self.prefix = self.name.title()
    self.config_dir = os.getcwd()
    self.stack_name = self.name.lower()
    self.build_dir = os.path.join(self.config_dir, 'build')
    self.template = {'AWSTemplateFormatVersion': '2010-09-09', 'Transform': 'AWS::Serverless-2016-10-31', 'Description': f'ASGI application updated @ {datetime.datetime.now()}', 'Globals': {'Function': {'Timeout': self.timeout}}, 'Parameters': {}, 'Resources': {}, 'Outputs': {}}
    self.generate_template()
