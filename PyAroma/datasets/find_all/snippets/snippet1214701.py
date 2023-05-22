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
@argument('identifiers', nargs=(- 1), metavar='REPO')
@option('--nopull', is_flag=True, help='Do not use `git pull` or other things that require internet access')
@option('--only', '-o', multiple=True, help='Only process the named sections (whole names only)')
@option('--quick', is_flag=True, help='Skip every @section except those marked with quick=True')
@_globals
def update(identifiers, nopull, only, quick):
    "\n    Performs a `git pull` in each of the repositories registered with\n    `homely add`, runs all of their HOMELY.py scripts, and then performs\n    automatic cleanup as necessary.\n\n    REPO\n        This should be the path to a local dotfiles repository that has already\n        been registered using `homely add`. If you specify one or more `REPO`s\n        then only the HOMELY.py scripts from those repositories will be run,\n        and automatic cleanup will not be performed (automatic cleanup is only\n        possible when homely has done an update of all repositories in one go).\n        If you do not specify a REPO, all repositories' HOMELY.py scripts will\n        be run.\n\n    The --nopull and --only options are useful when you are working on your\n    HOMELY.py script - the --nopull option stops you from wasting time checking\n    the internet for the same updates on every run, and the --only option\n    allows you to execute only the section you are working on.\n    "
    mkcfgdir()
    setallowpull((not nopull))
    cfg = RepoListConfig()
    if len(identifiers):
        updatedict = {}
        for identifier in identifiers:
            repo = cfg.find_by_any(identifier, 'ilc')
            if (repo is None):
                hint = ('Try running %s add /path/to/this/repo first' % CMD)
                raise Fatal(('Unrecognised repo %s (%s)' % (identifier, hint)))
            updatedict[repo.repoid] = repo
        updatelist = updatedict.values()
        cleanup = (len(updatelist) == cfg.repo_count())
    else:
        updatelist = list(cfg.find_all())
        cleanup = True
    success = run_update(updatelist, pullfirst=(not nopull), only=only, quick=quick, cancleanup=(cleanup and (not quick)))
    if (not success):
        sys.exit(1)
