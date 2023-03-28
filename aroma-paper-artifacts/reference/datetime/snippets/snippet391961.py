from __future__ import print_function, unicode_literals, division, absolute_import
import os, sys, json, subprocess, pipes
import collections, datetime
import dxpy
from .describe import get_field_from_jbor, get_job_from_jbor, get_index_from_jbor, is_job_ref, job_output_to_str, JOB_STATES
from .printing import GREEN, BLUE, BOLD, ENDC, fill
from .resolver import is_localjob_id
from ..compat import open, str, environ, USING_PYTHON2, basestring
from . import file_load_utils


def run_one_entry_point(job_id, function, input_hash, run_spec, depends_on, name=None):
    "\n    :param job_id: job ID of the local job to run\n    :type job_id: string\n    :param function: function to run\n    :type function: string\n    :param input_hash: input for the job (may include job-based object references)\n    :type input_hash: dict\n    :param run_spec: run specification from the dxapp.json of the app\n    :type run_spec: dict\n\n    Runs the specified entry point and retrieves the job's output,\n    updating job_outputs.json (in $DX_TEST_JOB_HOMEDIRS) appropriately.\n    "
    print('======')
    job_homedir = os.path.join(environ['DX_TEST_JOB_HOMEDIRS'], job_id)
    job_env = environ.copy()
    job_env['HOME'] = os.path.join(environ['DX_TEST_JOB_HOMEDIRS'], job_id)
    all_job_outputs_path = os.path.join(environ['DX_TEST_JOB_HOMEDIRS'], 'job_outputs.json')
    with open(all_job_outputs_path, 'r') as fd:
        all_job_outputs = json.load(fd, object_pairs_hook=collections.OrderedDict)
    if isinstance(name, basestring):
        name += ((((' (' + job_id) + ':') + function) + ')')
    else:
        name = ((job_id + ':') + function)
    job_name = (((BLUE() + BOLD()) + name) + ENDC())
    print(job_name)
    try:
        resolve_job_references(input_hash, all_job_outputs)
    except Exception as e:
        exit_with_error(((((job_name + ' ') + JOB_STATES('failed')) + ' when resolving input:\n') + fill(str(e))))
    if (depends_on is None):
        depends_on = []
    get_implicit_depends_on(input_hash, depends_on)
    try:
        wait_for_depends_on(depends_on, all_job_outputs)
    except Exception as e:
        exit_with_error(((((job_name + ' ') + JOB_STATES('failed')) + ' when processing depends_on:\n') + fill(str(e))))
    with open(os.path.join(job_homedir, 'job_input.json'), 'w') as fd:
        json.dump(input_hash, fd, indent=4)
        fd.write('\n')
    print(job_output_to_str(input_hash, title=((BOLD() + 'Input: ') + ENDC()), title_len=len('Input: ')).lstrip())
    if (run_spec['interpreter'] == 'bash'):
        env_path = os.path.join(job_homedir, 'environment')
        with open(env_path, 'w') as fd:
            job_input_file = os.path.join(job_homedir, 'job_input.json')
            var_defs_hash = file_load_utils.gen_bash_vars(job_input_file, job_homedir=job_homedir)
            for (key, val) in list(var_defs_hash.items()):
                fd.write('{}={}\n'.format(key, val))
    print(((BOLD() + 'Logs:') + ENDC()))
    start_time = datetime.datetime.now()
    if (run_spec['interpreter'] == 'bash'):
        script = '\n          cd {homedir};\n          . {env_path};\n          . {code_path};\n          if [[ $(type -t {function}) == "function" ]];\n          then {function};\n          else echo "$0: Global scope execution complete. Not invoking entry point function {function} because it was not found" 1>&2;\n          fi'.format(homedir=pipes.quote(job_homedir), env_path=pipes.quote(os.path.join(job_env['HOME'], 'environment')), code_path=pipes.quote(environ['DX_TEST_CODE_PATH']), function=function)
        invocation_args = ((['bash', '-c', '-e'] + (['-x'] if environ.get('DX_TEST_X_FLAG') else [])) + [script])
    elif (run_spec['interpreter'] == 'python2.7'):
        script = '#!/usr/bin/env python\nimport os\nos.chdir({homedir})\n\n{code}\n\nimport dxpy, json\nif dxpy.utils.exec_utils.RUN_COUNT == 0:\n    dxpy.run()\n'.format(homedir=repr(job_homedir), code=run_spec['code'])
        job_env['DX_TEST_FUNCTION'] = function
        invocation_args = ['python', '-c', script]
    if USING_PYTHON2:
        invocation_args = [arg.encode(sys.stdout.encoding) for arg in invocation_args]
        env = {k: v.encode(sys.stdout.encoding) for (k, v) in job_env.items()}
    else:
        env = job_env
    fn_process = subprocess.Popen(invocation_args, env=env)
    fn_process.communicate()
    end_time = datetime.datetime.now()
    if (fn_process.returncode != 0):
        exit_with_error(((((((job_name + ' ') + JOB_STATES('failed')) + ', exited with error code ') + str(fn_process.returncode)) + ' after ') + str((end_time - start_time))))
    job_output_path = os.path.join(job_env['HOME'], 'job_output.json')
    if os.path.exists(job_output_path):
        try:
            with open(job_output_path, 'r') as fd:
                job_output = json.load(fd, object_pairs_hook=collections.OrderedDict)
        except Exception as e:
            exit_with_error(((('Error: Could not load output of ' + job_name) + ':\n') + fill(((str(e.__class__) + ': ') + str(e)))))
    else:
        job_output = {}
    print(((((((job_name + ' -> ') + GREEN()) + 'finished running') + ENDC()) + ' after ') + str((end_time - start_time))))
    print(job_output_to_str(job_output, title=((BOLD() + 'Output: ') + ENDC()), title_len=len('Output: ')).lstrip())
    with open(os.path.join(environ['DX_TEST_JOB_HOMEDIRS'], 'job_outputs.json'), 'r') as fd:
        all_job_outputs = json.load(fd, object_pairs_hook=collections.OrderedDict)
    all_job_outputs[job_id] = job_output
    for other_job_id in all_job_outputs:
        if (all_job_outputs[other_job_id] is None):
            continue
        resolve_job_references(all_job_outputs[other_job_id], all_job_outputs, should_resolve=False)
    with open(os.path.join(environ['DX_TEST_JOB_HOMEDIRS'], 'job_outputs.json'), write_mode) as fd:
        json.dump(all_job_outputs, fd, indent=4)
        fd.write(eol)
