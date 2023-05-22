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
@option('--pause', is_flag=True, help='Pause automatic updates. This can be useful while you are working on your HOMELY.py script')
@option('--unpause', is_flag=True, help='Un-pause automatic updates')
@option('--outfile', is_flag=True, help="Prints the _path_ of the file containing the output of the previous 'homely update' run that was initiated by autoupdate.")
@option('--daemon', is_flag=True, help="Starts a 'homely update' daemon process, as long as it hasn't been run too recently")
@option('--clear', is_flag=True, help='Clear any previous update error so that autoupdate can initiate updates again.')
@_globals
def autoupdate(**kwargs):
    options = ('pause', 'unpause', 'outfile', 'daemon', 'clear')
    action = None
    for name in options:
        if kwargs[name]:
            if (action is not None):
                raise UsageError(('--%s and --%s options cannot be combined' % (action, name)))
            action = name
    if (action is None):
        raise UsageError(('Either %s must be used' % ' or '.join(('--{}'.format(o) for o in options))))
    mkcfgdir()
    if (action == 'pause'):
        with open(PAUSEFILE, 'w'):
            pass
        return
    if (action == 'unpause'):
        if os.path.exists(PAUSEFILE):
            os.unlink(PAUSEFILE)
        return
    if (action == 'clear'):
        if os.path.exists(FAILFILE):
            os.unlink(FAILFILE)
        return
    if (action == 'outfile'):
        print(OUTFILE)
        return
    assert (action == 'daemon')
    (status, mtime, _) = getstatus()
    if (status == UpdateStatus.FAILED):
        print("Can't start daemon - previous update failed")
        sys.exit(1)
    if (status == UpdateStatus.PAUSED):
        print("Can't start daemon - updates are paused")
        sys.exit(1)
    if (status == UpdateStatus.RUNNING):
        print("Can't start daemon - an update is already running")
        sys.exit(1)
    interval = ((20 * 60) * 60)
    if ((mtime is not None) and ((time.time() - mtime) < interval)):
        print("Can't start daemon - too soon to start another update")
        sys.exit(1)
    assert (status in (UpdateStatus.OK, UpdateStatus.NEVER, UpdateStatus.NOCONN))
    oldcwd = os.getcwd()
    import daemon
    with daemon.DaemonContext(), open(OUTFILE, 'w') as f:
        try:
            from homely._ui import setstreams
            setstreams(f, f)
            if (sys.version_info[0] < 3):
                os.chdir(oldcwd)
            cfg = RepoListConfig()
            run_update(list(cfg.find_all()), pullfirst=True, quick=False, cancleanup=True)
        except Exception:
            import traceback
            f.write(traceback.format_exc())
            raise
