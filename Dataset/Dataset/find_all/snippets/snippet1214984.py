import os
import shutil
import tempfile
import time
from homely._utils import opentext
import inspect
from homely._ui import run_update
from homely._utils import RepoListConfig


def run_update_all(pullfirst=False, cancleanup=False, quick=False) -> None:
    from homely._ui import run_update
    from homely._utils import RepoListConfig
    cfg = RepoListConfig()
    success = run_update(list(cfg.find_all()), pullfirst=pullfirst, only=None, cancleanup=cancleanup, quick=quick)
    assert success, 'run_update() encountered errors or warnings'
