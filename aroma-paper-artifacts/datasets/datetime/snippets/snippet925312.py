import argparse
import datetime
import functools
import json
import multiprocessing
import os
import signal
import warnings
from pathlib import Path
import git
import pygments.lexers
from tqdm import tqdm
from wcmatch import fnmatch


def analyze_cmdline():
    parser = argparse.ArgumentParser(description='Analyze git repo')
    parser.add_argument('--cohortfm', default='%Y', type=str, help='A Python datetime format string such as "%%Y" for creating cohorts (default: %(default)s)')
    parser.add_argument('--interval', default=(((7 * 24) * 60) * 60), type=int, help='Min difference between commits to analyze (default: %(default)ss)')
    parser.add_argument('--ignore', default=[], action='append', help="File patterns that should be ignored (can provide multiple, will each subtract independently). Uses glob syntax and generally needs to be shell escaped. For instance, to ignore a subdirectory `foo/`, run `git-of-theseus . --ignore 'foo/**'`.")
    parser.add_argument('--only', default=[], action='append', help="File patterns that can match. Multiple can be provided. If at least one is provided, every file has to match at least one. Uses glob syntax and typically has to be shell escaped. In order to analytize a subdirectory `bar/`, run `git-of-theseus . --only 'bar/**'`")
    parser.add_argument('--outdir', default='.', help='Output directory to store results (default: %(default)s)')
    parser.add_argument('--branch', default='master', type=str, help='Branch to track (default: %(default)s)')
    parser.add_argument('--ignore-whitespace', default=[], action='store_true', help='Ignore whitespace changes when running git blame.')
    parser.add_argument('--all-filetypes', action='store_true', help=('Include all files (if not set then will only analyze %s' % ','.join(default_filetypes)))
    parser.add_argument('--quiet', action='store_true', help='Disable all console output (default: %(default)s)')
    parser.add_argument('--procs', default=2, type=int, help='Number of processes to use. There is a point of diminishing returns, and RAM may become an issue on large repos (default: %(default)s)')
    parser.add_argument('--opt', action='store_true', help='Generates git commit-graph; Improves performance at the cost of some (~80KB/kCommit) disk space (default: %(default)s)')
    parser.add_argument('repo_dir')
    kwargs = vars(parser.parse_args())
    try:
        analyze(**kwargs)
    except KeyboardInterrupt:
        exit(1)
    except:
        raise
