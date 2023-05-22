import os
import sys
import time
from click import UsageError, argument, echo, group, option, version_option
from homely import version
from homely._errors import ERR_NO_COMMITS, ERR_NOT_A_REPO, JsonError, NotARepo, RepoHasNoCommitsError
from homely._ui import PROMPT_ALWAYS, PROMPT_NEVER, addfromremote, note, run_update, setallowpull, setverbose, setwantprompt, warn
from homely._utils import FAILFILE, OUTFILE, PAUSEFILE, STATUSCODES, RepoInfo, RepoListConfig, UpdateStatus, getstatus, mkcfgdir, saveconfig
from homely._vcs import getrepohandler
import daemon
from homely._ui import setstreams
import traceback


@homely.command()
@option('--format', '-f', default='%(repoid)s: %(localpath)s', help='Format string for the output, which will be passed through str.format(). You may use the following named replacements:\n%(repoid)s\n%(localpath)s\n%(canonical)s')
@_globals
def repolist(format):
    cfg = RepoListConfig()
    for info in cfg.find_all():
        vars_ = dict(repoid=info.repoid, localpath=info.localrepo.repo_path, canonical=(info.canonicalrepo.repo_path if info.canonicalrepo else ''))
        print((format % vars_))
