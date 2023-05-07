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


def analyze(repo_dir, cohortfm='%Y', interval=(((7 * 24) * 60) * 60), ignore=[], only=[], outdir='.', branch='master', all_filetypes=False, ignore_whitespace=False, procs=2, quiet=False, opt=False):
    use_mailmap = (Path(repo_dir) / '.mailmap').exists()
    repo = git.Repo(repo_dir)
    blame_kwargs = {}
    if ignore_whitespace:
        blame_kwargs['w'] = True
    master_commits = []
    commit2cohort = {}
    curve_key_tuples = set()
    tqdm_args = {'smoothing': 0.025, 'disable': quiet, 'dynamic_ncols': True}
    if (not os.path.exists(outdir)):
        os.makedirs(outdir)
    try:
        repo.git.show_ref('refs/heads/{:s}'.format(branch), verify=True)
    except git.exc.GitCommandError:
        default_branch = repo.active_branch.name
        warnings.warn("Requested branch: '{:s}' does not exist. Falling back to default branch: '{:s}'".format(branch, default_branch))
        branch = default_branch
    if ((not quiet) and (repo.git.version_info < (2, 31, 0))):
        print('Old Git version {:d}.{:d}.{:d} detected. There are optimizations available in version 2.31.0 which speed up performance'.format(*repo.git.version_info))
    if opt:
        if (not quiet):
            print('Generating git commit-graph... If you wish, this file is deletable later at .git/objects/info')
        repo.git.execute(['git', 'commit-graph', 'write', '--changed-paths'])
    desc = '{:<55s}'.format('Listing all commits')
    for commit in tqdm(repo.iter_commits(branch), desc=desc, unit=' Commits', **tqdm_args):
        cohort = datetime.datetime.utcfromtimestamp(commit.committed_date).strftime(cohortfm)
        commit2cohort[commit.binsha] = cohort
        curve_key_tuples.add(('cohort', cohort))
        if use_mailmap:
            (author_name, author_email) = get_mailmap_author_name_email(repo, commit.author.name, commit.author.email)
        else:
            (author_name, author_email) = (commit.author.name, commit.author.email)
        curve_key_tuples.add(('author', author_name))
        curve_key_tuples.add(('domain', author_email.split('@')[(- 1)]))
    desc = '{:<55s}'.format('Backtracking the master branch')
    with tqdm(desc=desc, unit=' Commits', **tqdm_args) as bar:
        commit = repo.head.commit
        last_date = None
        while True:
            if ((last_date is None) or (commit.committed_date < (last_date - interval))):
                master_commits.append(commit)
                last_date = commit.committed_date
            bar.update()
            if (not commit.parents):
                break
            commit = commit.parents[0]
        del commit
    if (ignore and (not only)):
        only = ['**']
    def_ft_str = '+({:s})'.format('|'.join(default_filetypes))
    path_match_str = '{:s}|!+({:s})'.format('|'.join(only), '|'.join(ignore))
    path_match_zero = ((len(only) == 0) and (len(ignore) == 0))
    ok_entry_paths = dict()
    all_entries = []

    def entry_path_ok(path):
        if (path not in ok_entry_paths):
            ok_entry_paths[path] = ((all_filetypes or fnmatch.fnmatch(os.path.split(path)[(- 1)], def_ft_str, flags=fnmatch.EXTMATCH)) and (path_match_zero or fnmatch.fnmatch(path, path_match_str, flags=((fnmatch.NEGATE | fnmatch.EXTMATCH) | fnmatch.SPLIT))))
        return ok_entry_paths[path]

    def get_entries(commit):
        tmp = [MiniEntry(entry) for entry in commit.tree.traverse() if ((entry.type == 'blob') and entry_path_ok(entry.path))]
        all_entries.append(tmp)
        return tmp
    master_commits = master_commits[::(- 1)]
    entries_total = 0
    desc = '{:<55s}'.format('Discovering entries & caching filenames')
    with tqdm(desc='{:<55s}'.format('Entries Discovered'), unit=' Entries', position=1, **tqdm_args) as bar:
        for (i, commit) in enumerate(tqdm(master_commits, desc=desc, unit=' Commits', position=0, **tqdm_args)):
            for entry in get_entries(commit):
                entries_total += 1
                (_, ext) = os.path.splitext(entry.path)
                curve_key_tuples.add(('ext', ext))
                curve_key_tuples.add(('dir', get_top_dir(entry.path)))
                bar.update()
            master_commits[i] = MiniCommit(commit)
    del repo
    del ok_entry_paths
    del commit
    curves = {}
    ts = []
    last_file_y = {}
    cur_y = {}
    blamer = BlameDriver(repo_dir, procs, last_file_y, cur_y, blame_kwargs, commit2cohort, use_mailmap, quiet)
    commit_history = {}
    last_file_hash = {}

    def handler(a, b):
        try:
            blamer.pause()
            print('\n\nProcess paused')
            x = int(input('0. Exit\n1. Continue\n2. Modify process count\nSelect an option: '))
            if (x == 1):
                return blamer.resume()
            elif (x == 2):
                x = int(input('\n\nCurrent Processes: {:d}\nNew Setting: '.format(blamer.proc_count)))
                if (x > 0):
                    blamer.proc_count = x
                    blamer.spawn_process(spawn_only=True)
                return blamer.resume()
            os._exit(1)
        except:
            pass
        handler(None, None)
    if (not quiet):
        signal.signal(signal.SIGINT, handler)
    desc = '{:<55s}'.format('Analyzing commit history with {:d} processes'.format(procs))
    with tqdm(desc='{:<55s}'.format('Entries Processed'), total=entries_total, unit=' Entries', position=1, maxinterval=1, miniters=100, **tqdm_args) as bar:
        cbar = tqdm(master_commits, desc=desc, unit=' Commits', position=0, **tqdm_args)
        for commit in cbar:
            t = datetime.datetime.utcfromtimestamp(commit.committed_date)
            ts.append(t)
            entries = all_entries.pop(0)
            check_entries = []
            cur_file_hash = {}
            for entry in entries:
                cur_file_hash[entry.path] = entry.binsha
                if (entry.path in last_file_hash):
                    if (last_file_hash[entry.path] != entry.binsha):
                        for (key_tuple, count) in last_file_y[entry.path].items():
                            cur_y[key_tuple] -= count
                        check_entries.append(entry)
                    else:
                        bar.update()
                    del last_file_hash[entry.path]
                else:
                    check_entries.append(entry)
            for deleted_path in last_file_hash.keys():
                for (key_tuple, count) in last_file_y[deleted_path].items():
                    cur_y[key_tuple] -= count
            last_file_hash = cur_file_hash
            blamer.fetch(commit, check_entries, bar)
            cbar.set_description('{:<55s}'.format('Analyzing commit history with {:d} processes'.format(len(blamer.proc_pool))), False)
            for (key_tuple, count) in cur_y.items():
                (key_category, key) = key_tuple
                if (key_category == 'sha'):
                    commit_history.setdefault(key, []).append((commit.committed_date, count))
            for key_tuple in curve_key_tuples:
                curves.setdefault(key_tuple, []).append(cur_y.get(key_tuple, 0))
    signal.signal(signal.SIGINT, signal.default_int_handler)

    def dump_json(output_fn, key_type, label_fmt=(lambda x: x)):
        key_items = sorted((k for (t, k) in curve_key_tuples if (t == key_type)))
        fn = os.path.join(outdir, output_fn)
        if (not quiet):
            print(('Writing %s data to %s' % (key_type, fn)))
        f = open(fn, 'w')
        json.dump({'y': [curves[(key_type, key_item)] for key_item in key_items], 'ts': [t.isoformat() for t in ts], 'labels': [label_fmt(key_item) for key_item in key_items]}, f)
        f.close()
    dump_json('cohorts.json', 'cohort', (lambda c: ('Code added in %s' % c)))
    dump_json('exts.json', 'ext')
    dump_json('authors.json', 'author')
    dump_json('dirs.json', 'dir')
    dump_json('domains.json', 'domain')
    fn = os.path.join(outdir, 'survival.json')
    f = open(fn, 'w')
    if (not quiet):
        print(('Writing survival data to %s' % fn))
    json.dump(commit_history, f)
    f.close()
