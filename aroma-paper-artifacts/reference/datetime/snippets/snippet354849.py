import argparse
import datetime
from hashlib import md5
from importlib import import_module
from os import path, makedirs, listdir, getcwd
from shutil import copytree
from subprocess import Popen, PIPE, TimeoutExpired
import sys
from time import time
import ray


def main_inner(*, arch_mod, prob_mod, job_ncpus, enforce_job_ncpus, resume_from=None, restrict_test_probs=None):
    run_asnets_ray = ray.remote(num_cpus=job_ncpus)(run_asnets_local)
    root_cwd = getcwd()
    arch_name = arch_mod.__name__
    prob_name = prob_mod.__name__
    if (resume_from is None):
        time_str = datetime.datetime.now().isoformat()
        prefix_dir = ('experiment-results/%s-%s-%s' % (prob_name, arch_name, time_str))
        prefix_dir = path.join(root_cwd, prefix_dir)
        print(('Will put everything in %s' % prefix_dir))
        print('\n\n\n\n\n\nTraining network')
        train_flags = ['-e', prefix_dir]
        train_flags.extend(build_arch_flags(arch_mod, is_train=True))
        train_flags.extend(build_prob_flags_train(prob_mod))
        final_checkpoint = ray.get(run_asnets_ray.remote(flags=train_flags, cwd=root_cwd, root_dir=prefix_dir, need_snapshot=True, is_train=True, enforce_ncpus=enforce_job_ncpus, timeout=arch_mod.TIME_LIMIT_SECONDS))
        print(('Last valid checkpoint is %s' % final_checkpoint))
    else:
        final_checkpoint = resume_from
        prefix_dir = get_prefix_dir(final_checkpoint)
        print(('Resuming from checkpoint "%s"' % final_checkpoint))
        print(('Using experiment dir "%s"' % prefix_dir))
    print('\n\n\n\n\n\nTesting network')
    main_test_flags = ['--no-train', '--minimal-file-saves', '--resume-from', final_checkpoint, '-e', prefix_dir]
    main_test_flags.extend(build_arch_flags(arch_mod, is_train=False))
    print('Starting test loop')
    prob_flag_list = build_prob_flags_test(prob_mod, restrict_test_probs)
    job_infos = {}
    for (prob_idx, test_prob_flags) in prob_flag_list:
        print(('Launching test on problem %d' % (prob_idx + 1)))
        full_flags = (main_test_flags + test_prob_flags)
        job = run_asnets_ray.remote(flags=full_flags, root_dir=prefix_dir, cwd=root_cwd, need_snapshot=False, is_train=False, enforce_ncpus=enforce_job_ncpus, timeout=(arch_mod.EVAL_TIME_LIMIT_SECONDS + 30))
        job_infos[job] = (prob_idx, test_prob_flags)
    print('Waiting for jobs to finish')
    remaining = list(job_infos)
    while remaining:
        ((ready,), remaining) = ray.wait(remaining, num_returns=1)
        (prob_idx, test_prob_flags) = job_infos[ready]
        print(('Finished job %d (flags: %s)' % (prob_idx, test_prob_flags)))
    return prefix_dir
