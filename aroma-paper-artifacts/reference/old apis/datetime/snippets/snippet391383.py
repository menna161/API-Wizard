from __future__ import print_function, unicode_literals, division, absolute_import
import datetime, time, json, math, sys, copy
import locale
import subprocess
from collections import defaultdict
import dxpy
from .printing import RED, GREEN, BLUE, YELLOW, WHITE, BOLD, UNDERLINE, ENDC, DELIMITER, get_delimiter, fill
from .pretty_print import format_timedelta
from ..compat import basestring, USING_PYTHON2
from ..bindings.search import find_one_data_object
from ..exceptions import DXError
from dxpy.api import job_describe


def get_find_executions_string(desc, has_children, single_result=False, show_outputs=True, is_cached_result=False):
    "\n    :param desc: hash of execution's describe output\n    :param has_children: whether the execution has children to be printed\n    :param single_result: whether the execution is displayed as a single result or as part of an execution tree\n    :param is_cached_result: whether the execution should be formatted as a cached result\n    "
    is_not_subjob = ((desc['parentJob'] is None) or (desc['class'] == 'analysis') or single_result)
    result = ('* ' if (is_not_subjob and (get_delimiter() is None)) else '')
    canonical_execution_name = desc['executableName']
    if (desc['class'] == 'job'):
        canonical_execution_name += (':' + desc['function'])
    execution_name = desc.get('name', '<no name>')
    if is_cached_result:
        result += ((BOLD() + '[') + ENDC())
    result += (BOLD() + BLUE())
    if (desc['class'] == 'analysis'):
        result += UNDERLINE()
    result += (execution_name + ENDC())
    if ((execution_name != canonical_execution_name) and ((execution_name + ':main') != canonical_execution_name)):
        result += ((' (' + canonical_execution_name) + ')')
    if is_cached_result:
        result += ((BOLD() + ']') + ENDC())
    result += (((DELIMITER(' (') + JOB_STATES(desc['state'])) + DELIMITER(') ')) + desc['id'])
    result += DELIMITER(('\n' + (u'│ ' if (is_not_subjob and has_children) else ('  ' if is_not_subjob else ''))))
    result += (desc['launchedBy'][5:] + DELIMITER(' '))
    result += render_short_timestamp(desc['created'])
    cached_and_runtime_strs = []
    if is_cached_result:
        cached_and_runtime_strs.append(((YELLOW() + 'cached') + ENDC()))
    if (desc['class'] == 'job'):
        if desc.get('startedRunning'):
            if (desc['state'] in ['done', 'failed', 'terminated', 'waiting_on_output']):
                runtime = datetime.timedelta(seconds=(int((desc['stoppedRunning'] - desc['startedRunning'])) // 1000))
                cached_and_runtime_strs.append(('runtime ' + str(runtime)))
            elif (desc['state'] == 'running'):
                seconds_running = max(int((time.time() - (desc['startedRunning'] // 1000))), 0)
                msg = 'running for {rt}'.format(rt=datetime.timedelta(seconds=seconds_running))
                cached_and_runtime_strs.append(msg)
    if cached_and_runtime_strs:
        result += ((' (' + ', '.join(cached_and_runtime_strs)) + ')')
    if show_outputs:
        prefix = DELIMITER(('\n' + (u'│ ' if (is_not_subjob and has_children) else ('  ' if is_not_subjob else ''))))
        if (desc.get('output') != None):
            result += job_output_to_str(desc['output'], prefix=prefix)
        elif ((desc['state'] == 'failed') and ('failureReason' in desc)):
            result += (((((prefix + BOLD()) + desc['failureReason']) + ENDC()) + ': ') + fill(desc.get('failureMessage', ''), subsequent_indent=prefix.lstrip('\n')))
    return result
