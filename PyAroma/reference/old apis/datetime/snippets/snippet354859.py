import collections
import datetime
import functools
import hashlib
import itertools
import math
import json
import os
import random
import re
import struct
import subprocess
import time
import click
import ray
from asnets.scripts.run_det_baselines import get_module_test_problems, wait_all_unordered, ray_setup, ASNETS_ROOT
from asnets.pddl_utils import extract_domain_problem, extract_domain_name
from asnets.ssipp_interface import get_ssipp_solver_path_auto


@click.command(help='run probabilistic baseline planners using Ray')
@click.argument('problem_module_name')
@click.option('--ssipp-path', default=None, type=str, help='path to SSiPP solver_ssp')
@click.option('--repeat', '-r', default=30, help='number of times to repeat experiment')
@click.option('--out-dir', '-o', default='./experiment-results/baselines-prob/', help='output directory to put results in')
@click.option('--max-sec-per-run', default=((3 * 60) * 60), help='maximum duration of a single planner execution (in seconds)')
@click.option('--max-sec-per-problem', default=((3 * 60) * 60), help='maximum duration of all executions on a problem (in seconds)')
@click.option('--ray-connect', default=None, type=str, help='connect Ray to this Redis DB instead of starting new cluster')
@click.option('--ray-ncpus', default=None, type=int, help='restrict Ray pool to use this many CPUs *in total* (only valid if spinning up new Ray cluster)')
def main(problem_module_name, ssipp_path, repeat, out_dir, max_sec_per_run, max_sec_per_problem, ray_connect, ray_ncpus):
    assert (0 < max_sec_per_run <= max_sec_per_problem), 'must have 0 < --max-sec-per-run <= --max-sec-per-problem'
    os.chdir(ASNETS_ROOT)
    ssipp_path = (ssipp_path or get_ssipp_solver_path_auto())
    print(('Assuming SSiPP at %s' % (ssipp_path,)))
    ray_setup(ray_connect, ray_ncpus)
    print(('Importing problem from %s' % problem_module_name))
    (domain_path, test_prob_paths_raw) = get_module_test_problems(problem_module_name)
    domain_name = extract_domain_name(domain_path)
    all_problems = []
    for (test_prob_path, prob_name) in test_prob_paths_raw:
        if (prob_name is None):
            (_, _, _, prob_name) = extract_domain_problem([domain_path, test_prob_path])
        all_problems.append((test_prob_path, prob_name))
    print('Launching tasks')
    task_partials = []
    for (problem_path, problem_name) in all_problems:
        for (planner, heuristic) in PLANNERS:
            partial = functools.partial(do_experiment.remote, planner, heuristic, domain_path, problem_path, problem_name, ssipp_path, max_sec_per_run, max_sec_per_problem, repeat)
            task_partials.append(partial)
    random.shuffle(task_partials)
    tasks = [part() for part in task_partials]
    finished_jobs = wait_all_unordered(tasks)
    out_dict = {}
    for (any_success, problem_name, singleton_dict) in finished_jobs:
        out_dict.setdefault(problem_name, {}).update(singleton_dict)
    out_dict = sort_dict({k: sort_dict(v) for (k, v) in out_dict.items()})
    date_str = datetime.datetime.now().isoformat()
    out_fn = ('results-%s-%ds-%s.json' % (domain_name, max_sec_per_problem, date_str))
    out_path = os.path.join(out_dir, out_fn)
    os.makedirs(out_dir, exist_ok=True)
    print(("Writing output to '%s'" % (out_path,)))
    with open(out_path, 'w') as out_fp:
        json.dump(out_dict, out_fp)
