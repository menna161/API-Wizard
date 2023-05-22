from __future__ import print_function, unicode_literals, division, absolute_import
import os, sys, datetime, getpass, collections, re, json, argparse, copy, hashlib, io, time, subprocess, glob, logging, functools, platform
import shlex
import requests
import csv
from ..compat import USING_PYTHON2, basestring, str, input, wrap_stdio_in_codecs, decode_command_line_args, unwrap_stream, sys_encoding
import dxpy
from dxpy.scripts import dx_build_app
from dxpy import workflow_builder
from dxpy.exceptions import PermissionDenied, InvalidState, ResourceNotFound
from ..cli import try_call, prompt_for_yn, INTERACTIVE_CLI
from ..cli import workflow as workflow_cli
from ..cli.cp import cp
from ..cli.dataset_utilities import extract_dataset
from ..cli.download import download_one_file, download_one_database_file, download
from ..cli.parsers import no_color_arg, delim_arg, env_args, stdout_args, all_arg, json_arg, parser_dataobject_args, parser_single_dataobject_output_args, process_properties_args, find_by_properties_and_tags_args, process_find_by_property_args, process_dataobject_args, process_single_dataobject_output_args, find_executions_args, add_find_executions_search_gp, set_env_from_args, extra_args, process_extra_args, DXParserError, exec_input_args, instance_type_arg, process_instance_type_arg, process_instance_count_arg, get_update_project_args, property_args, tag_args, contains_phi, process_phi_param, process_external_upload_restricted_param
from ..cli.exec_io import ExecutableInputs, format_choices_or_suggestions
from ..cli.org import get_org_invite_args, add_membership, remove_membership, update_membership, new_org, update_org, find_orgs, org_find_members, org_find_projects, org_find_apps
from ..exceptions import err_exit, DXError, DXCLIError, DXAPIError, network_exceptions, default_expected_exceptions, format_exception
from ..utils import warn, group_array_by_field, normalize_timedelta, normalize_time_input
from ..utils.batch_utils import batch_run, batch_launch_args
from ..app_categories import APP_CATEGORIES
from ..utils.printing import CYAN, BLUE, YELLOW, GREEN, RED, WHITE, UNDERLINE, BOLD, ENDC, DNANEXUS_LOGO, DNANEXUS_X, set_colors, set_delimiter, get_delimiter, DELIMITER, fill, tty_rows, tty_cols, pager, format_find_results, nostderr
from ..utils.pretty_print import format_tree, format_table
from ..utils.resolver import clean_folder_path, pick, paginate_and_pick, is_hashid, is_data_obj_id, is_container_id, is_job_id, is_analysis_id, get_last_pos_of_char, resolve_container_id_or_name, resolve_path, resolve_existing_path, get_app_from_path, resolve_app, resolve_global_executable, get_exec_handler, split_unescaped, ResolutionError, resolve_to_objects_or_project, is_project_explicit, object_exists_in_project, is_jbor_str, parse_input_keyval
from ..utils.completer import path_completer, DXPathCompleter, DXAppCompleter, LocalCompleter, ListCompleter, MultiCompleter
from ..utils.describe import print_data_obj_desc, print_desc, print_ls_desc, get_ls_l_desc, print_ls_l_header, print_ls_l_desc, get_ls_l_desc_fields, get_io_desc, get_find_executions_string
from ..system_requirements import SystemRequirementsDict
from ..asset_builder import build_asset
from ..ssh_tunnel_app_support import run_notebook
from ..ssh_tunnel_app_support import run_loupe
import colorama
from dxpy.utils.executable_unbuilder import dump_executable
from dxpy.utils.executable_unbuilder import dump_executable
from dxpy.utils.executable_unbuilder import dump_executable
from dxpy.utils.executable_unbuilder import dump_executable
from dxpy.utils.job_log_client import DXJobLogStreamClient
import socket
from xattr import xattr
import argcomplete
import pyreadline3 as readline
import gnureadline as readline
import itertools
from dxpy.utils import spelling_corrector
import readline


def watch(args):
    level_colors = {level: RED() for level in ('EMERG', 'ALERT', 'CRITICAL', 'ERROR')}
    level_colors.update({level: YELLOW() for level in ('WARNING', 'STDERR')})
    level_colors.update({level: GREEN() for level in ('NOTICE', 'INFO', 'DEBUG', 'STDOUT')})
    (msg_callback, log_client) = (None, None)
    if args.get_stdout:
        args.levels = ['STDOUT']
        args.format = '{msg}'
        args.job_info = False
    elif args.get_stderr:
        args.levels = ['STDERR']
        args.format = '{msg}'
        args.job_info = False
    elif args.get_streams:
        args.levels = ['STDOUT', 'STDERR']
        args.format = '{msg}'
        args.job_info = False
    elif (args.format is None):
        if args.job_ids:
            args.format = (((BLUE('{job_name} ({job})') + ' {level_color}{level}') + ENDC()) + ' {msg}')
        else:
            args.format = (((BLUE('{job_name}') + ' {level_color}{level}') + ENDC()) + ' {msg}')
        if args.timestamps:
            args.format = ('{timestamp} ' + args.format)

        def msg_callback(message):
            message['timestamp'] = str(datetime.datetime.fromtimestamp((message.get('timestamp', 0) // 1000)))
            message['level_color'] = level_colors.get(message.get('level', ''), '')
            message['job_name'] = (log_client.seen_jobs[message['job']]['name'] if (message['job'] in log_client.seen_jobs) else message['job'])
            print(args.format.format(**message))
    from dxpy.utils.job_log_client import DXJobLogStreamClient
    input_params = {'numRecentMessages': args.num_recent_messages, 'recurseJobs': args.tree, 'tail': args.tail}
    if args.levels:
        input_params['levels'] = args.levels
    if (not re.match('^job-[0-9a-zA-Z]{24}$', args.jobid)):
        err_exit((args.jobid + ' does not look like a DNAnexus job ID'))
    job_describe = dxpy.describe(args.jobid)
    if (('outputReusedFrom' in job_describe) and (job_describe['outputReusedFrom'] is not None)):
        args.jobid = job_describe['outputReusedFrom']
        if (not args.quiet):
            print(('Output reused from %s' % args.jobid))
    log_client = DXJobLogStreamClient(args.jobid, input_params=input_params, msg_callback=msg_callback, msg_output_format=args.format, print_job_info=args.job_info)
    try:
        if (not args.quiet):
            print(('Watching job %s%s. Press Ctrl+C to stop watching.' % (args.jobid, (' and sub-jobs' if args.tree else ''))), file=sys.stderr)
        log_client.connect()
    except Exception as details:
        err_exit(fill(str(details)), 3)
