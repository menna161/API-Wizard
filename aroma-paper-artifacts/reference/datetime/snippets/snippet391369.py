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


def print_execution_desc(desc):
    recognized_fields = ['id', 'class', 'project', 'workspace', 'region', 'app', 'applet', 'executable', 'workflow', 'state', 'rootExecution', 'parentAnalysis', 'parentJob', 'originJob', 'analysis', 'stage', 'function', 'runInput', 'originalInput', 'input', 'output', 'folder', 'launchedBy', 'created', 'modified', 'failureReason', 'failureMessage', 'stdout', 'stderr', 'waitingOnChildren', 'dependsOn', 'resources', 'projectCache', 'details', 'tags', 'properties', 'name', 'instanceType', 'systemRequirements', 'executableName', 'failureFrom', 'billTo', 'startedRunning', 'stoppedRunning', 'stateTransitions', 'delayWorkspaceDestruction', 'stages', 'totalPrice', 'isFree', 'invoiceMetadata', 'priority', 'sshHostKey', 'internetUsageIPs', 'spotWaitTime', 'maxTreeSpotWaitTime', 'maxJobSpotWaitTime']
    print_field('ID', desc['id'])
    print_field('Class', desc['class'])
    if (('name' in desc) and (desc['name'] is not None)):
        print_field('Job name', desc['name'])
    if (('executableName' in desc) and (desc['executableName'] is not None)):
        print_field('Executable name', desc['executableName'])
    print_field('Project context', desc['project'])
    if ('region' in desc):
        print_field('Region', desc['region'])
    if ('billTo' in desc):
        print_field('Billed to', desc['billTo'][(5 if desc['billTo'].startswith('user-') else 0):])
    if ('workspace' in desc):
        print_field('Workspace', desc['workspace'])
    if ('projectCache' in desc):
        print_field('Cache workspace', desc['projectCache'])
        print_field('Resources', desc['resources'])
    if ('app' in desc):
        print_field('App', desc['app'])
    elif desc.get('executable', '').startswith('globalworkflow'):
        print_field('Workflow', desc['executable'])
    elif ('applet' in desc):
        print_field('Applet', desc['applet'])
    elif ('workflow' in desc):
        print_field('Workflow', desc['workflow']['id'])
    if (('instanceType' in desc) and (desc['instanceType'] is not None)):
        print_field('Instance Type', desc['instanceType'])
    if ('priority' in desc):
        print_field('Priority', desc['priority'])
    print_field('State', JOB_STATES(desc['state']))
    if ('rootExecution' in desc):
        print_field('Root execution', desc['rootExecution'])
    if ('originJob' in desc):
        if (desc['originJob'] is None):
            print_field('Origin job', '-')
        else:
            print_field('Origin job', desc['originJob'])
    if (desc['parentJob'] is None):
        print_field('Parent job', '-')
    else:
        print_field('Parent job', desc['parentJob'])
    if ('parentAnalysis' in desc):
        if (desc['parentAnalysis'] is not None):
            print_field('Parent analysis', desc['parentAnalysis'])
    if (('analysis' in desc) and (desc['analysis'] is not None)):
        print_field('Analysis', desc['analysis'])
        print_field('Stage', desc['stage'])
    if ('stages' in desc):
        for (i, (stage, analysis_stage)) in enumerate(zip(desc['workflow']['stages'], desc['stages'])):
            stage['execution'] = analysis_stage['execution']
            render_stage(('Stage ' + str(i)), stage, as_stage_of=desc['id'])
    if ('function' in desc):
        print_field('Function', desc['function'])
    if ('runInput' in desc):
        default_fields = {k: v for (k, v) in desc['originalInput'].items() if (k not in desc['runInput'])}
        print_nofill_field('Input', get_io_field(desc['runInput'], defaults=default_fields))
    else:
        print_nofill_field('Input', get_io_field(desc['originalInput']))
    resolved_jbors = {}
    input_with_jbors = desc.get('runInput', desc['originalInput'])
    for k in desc['input']:
        if ((k in input_with_jbors) and (desc['input'][k] != input_with_jbors[k])):
            get_resolved_jbors(desc['input'][k], input_with_jbors[k], resolved_jbors)
    if (len(resolved_jbors) != 0):
        print_nofill_field('Resolved JBORs', get_io_field(resolved_jbors, delim=((GREEN() + '=>') + ENDC())))
    print_nofill_field('Output', get_io_field(desc['output']))
    if ('folder' in desc):
        print_field('Output folder', desc['folder'])
    print_field('Launched by', desc['launchedBy'][5:])
    print_field('Created', render_timestamp(desc['created']))
    if ('startedRunning' in desc):
        if ('stoppedRunning' in desc):
            print_field('Started running', render_timestamp(desc['startedRunning']))
        else:
            print_field('Started running', '{t} (running for {rt})'.format(t=render_timestamp(desc['startedRunning']), rt=datetime.timedelta(seconds=(int(time.time()) - (desc['startedRunning'] // 1000)))))
    if ('stoppedRunning' in desc):
        print_field('Stopped running', '{t} (Runtime: {rt})'.format(t=render_timestamp(desc['stoppedRunning']), rt=datetime.timedelta(seconds=((desc['stoppedRunning'] - desc['startedRunning']) // 1000))))
    if ((desc.get('class') == 'analysis') and ('stateTransitions' in desc) and desc['stateTransitions']):
        if (desc['stateTransitions'][(- 1)]['newState'] in ['done', 'failed', 'terminated']):
            print_field('Finished', '{t} (Wall-clock time: {wt})'.format(t=render_timestamp(desc['stateTransitions'][(- 1)]['setAt']), wt=datetime.timedelta(seconds=((desc['stateTransitions'][(- 1)]['setAt'] - desc['created']) // 1000))))
    print_field('Last modified', render_timestamp(desc['modified']))
    if ('waitingOnChildren' in desc):
        print_list_field('Pending subjobs', desc['waitingOnChildren'])
    if ('dependsOn' in desc):
        print_list_field('Depends on', desc['dependsOn'])
    if ('failureReason' in desc):
        print_field('Failure reason', desc['failureReason'])
    if ('failureMessage' in desc):
        print_field('Failure message', desc['failureMessage'])
    if (('failureFrom' in desc) and (desc['failureFrom'] is not None) and (desc['failureFrom']['id'] != desc['id'])):
        print_field('Failure is from', desc['failureFrom']['id'])
    if ('systemRequirements' in desc):
        print_json_field('Sys Requirements', desc['systemRequirements'])
    if ('tags' in desc):
        print_list_field('Tags', desc['tags'])
    if ('properties' in desc):
        print_list_field('Properties', [((key + '=') + value) for (key, value) in desc['properties'].items()])
    if (('details' in desc) and ('clonedFrom' in desc['details'])):
        cloned_hash = desc['details']['clonedFrom']
        if ('id' in cloned_hash):
            print_field('Re-run of', cloned_hash['id'])
            print_field(' named', cloned_hash['name'])
            same_executable = (cloned_hash['executable'] == desc.get('applet', desc.get('app', '')))
            print_field(' using', ((('' if same_executable else YELLOW()) + cloned_hash['executable']) + (' (same)' if same_executable else ENDC())))
            same_project = (cloned_hash['project'] == desc['project'])
            same_folder = ((cloned_hash['folder'] == desc['folder']) or (not same_project))
            print_field(' output folder', ((((((('' if same_project else YELLOW()) + cloned_hash['project']) + ('' if same_project else ENDC())) + ':') + ('' if same_folder else YELLOW())) + cloned_hash['folder']) + (' (same)' if (same_project and same_folder) else ('' if same_folder else ENDC()))))
            different_inputs = []
            for item in cloned_hash['runInput']:
                if (cloned_hash['runInput'][item] != desc['runInput'][item]):
                    different_inputs.append(item)
            print_nofill_field(' input', get_io_field(cloned_hash['runInput'], highlight_fields=different_inputs))
            cloned_sys_reqs = cloned_hash.get('systemRequirements')
            if isinstance(cloned_sys_reqs, dict):
                if (cloned_sys_reqs == desc.get('systemRequirements')):
                    print_nofill_field(' sys reqs', (json.dumps(cloned_sys_reqs) + ' (same)'))
                else:
                    print_nofill_field(' sys reqs', ((YELLOW() + json.dumps(cloned_sys_reqs)) + ENDC()))
    if ((not desc.get('isFree')) and (desc.get('totalPrice') is not None)):
        print_field('Total Price', format_currency(desc['totalPrice'], meta=desc['currency']))
    if (desc.get('spotWaitTime') is not None):
        print_field('Spot Wait Time', format_timedelta(desc.get('spotWaitTime'), in_seconds=True))
    if (desc.get('maxTreeSpotWaitTime') is not None):
        print_field('Max Tree Spot Wait Time', format_timedelta(desc.get('maxTreeSpotWaitTime'), in_seconds=True))
    if (desc.get('maxJobSpotWaitTime') is not None):
        print_field('Max Job Spot Wait Time', format_timedelta(desc.get('maxJobSpotWaitTime'), in_seconds=True))
    if desc.get('invoiceMetadata'):
        print_json_field('Invoice Metadata', desc['invoiceMetadata'])
    if desc.get('sshHostKey'):
        print_nofill_field('SSH Host Key', printable_ssh_host_key(desc['sshHostKey']))
    if ('internetUsageIPs' in desc):
        print_json_field('Internet Usage IPs', desc['internetUsageIPs'])
    for field in desc:
        if (field not in recognized_fields):
            print_json_field(field, desc[field])
