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


def login(args):
    if (not state['interactive']):
        args.save = True
    default_authserver = 'https://auth.dnanexus.com'
    using_default = False
    if (args.auth_token and (not args.token)):
        args.token = args.auth_token
        args.auth_token = None
    if (args.token is None):
        if ((args.host is None) != (args.port is None)):
            err_exit('Error: Only one of --host and --port were provided; provide either both or neither of the values', 2)
        authserver = dxpy.get_auth_server_name(args.host, args.port, args.protocol)
        using_default = (authserver == default_authserver)

        def get_token(**data):
            return dxpy.DXHTTPRequest((authserver + '/system/newAuthToken'), data, prepend_srv=False, auth=None, always_retry=True)

        def get_credentials(reuse=None, get_otp=False):
            if reuse:
                (username, password) = reuse
            else:
                username = None
                while (not username):
                    if ('DX_USERNAME' in os.environ):
                        username = (input((('Username [' + os.environ['DX_USERNAME']) + ']: ')) or os.environ['DX_USERNAME'])
                    else:
                        username = input('Username: ')
                dxpy.config.write('DX_USERNAME', username)
                with unwrap_stream('stdin'):
                    password = getpass.getpass()
            otp = (input('Verification code: ') if get_otp else None)
            return dict(username=username, password=password, otp=otp)
        print(('Acquiring credentials from ' + authserver))
        (attempt, using_otp, reuse) = (1, False, None)
        while (attempt <= 3):
            try:
                credentials = get_credentials(reuse=reuse, get_otp=using_otp)
                token_res = get_token(expires=normalize_time_input(args.timeout, future=True, default_unit='s'), **credentials)
                break
            except (KeyboardInterrupt, EOFError):
                err_exit()
            except dxpy.DXAPIError as e:
                if (e.name == 'OTPRequiredError'):
                    using_otp = True
                    reuse = (credentials['username'], credentials['password'])
                    continue
                elif (e.name in ('UsernameOrPasswordError', 'OTPMismatchError')):
                    if (attempt < 3):
                        if (e.name == 'UsernameOrPasswordError'):
                            warn('Incorrect username and/or password')
                        else:
                            warn('Incorrect verification code')
                        attempt += 1
                        continue
                    else:
                        err_exit('Incorrect username and/or password', arg_parser=parser)
                else:
                    err_exit('Login error: {}'.format(e), arg_parser=parser)
            except Exception as e:
                err_exit('Login error: {}'.format(e), arg_parser=parser)
        sec_context = json.dumps({'auth_token': token_res['access_token'], 'auth_token_type': token_res['token_type']})
        if using_default:
            set_api(dxpy.DEFAULT_APISERVER_PROTOCOL, dxpy.DEFAULT_APISERVER_HOST, dxpy.DEFAULT_APISERVER_PORT, args.save)
    else:
        sec_context = (('{"auth_token":"' + args.token) + '","auth_token_type":"Bearer"}')
        if (args.host is None):
            set_api(dxpy.DEFAULT_APISERVER_PROTOCOL, dxpy.DEFAULT_APISERVER_HOST, dxpy.DEFAULT_APISERVER_PORT, args.save)
            using_default = True
    os.environ['DX_SECURITY_CONTEXT'] = sec_context
    dxpy.set_security_context(json.loads(sec_context))
    if args.save:
        dxpy.config.write('DX_SECURITY_CONTEXT', sec_context)
    if (args.token is not None):
        (host, port) = (None, None)
        if (dxpy.APISERVER_HOST not in ['api.dnanexus.com', 'stagingapi.dnanexus.com']):
            (host, port) = (args.host, args.port)
        try:
            dxpy.config.write('DX_USERNAME', dxpy.user_info(host, port)['username'])
        except DXError as details:
            print('Could not obtain username from auth server. Consider setting both --host and --port.', file=sys.stderr)
            print(fill(str(details)), file=sys.stderr)
    if (using_default or args.staging):
        try:
            greeting = dxpy.api.system_greet({'client': 'dxclient', 'version': ('v' + dxpy.TOOLKIT_VERSION)})
            if greeting.get('messages'):
                print((BOLD('New messages from ') + DNANEXUS_LOGO()))
                for message in greeting['messages']:
                    print((BOLD('Date:    ') + datetime.datetime.fromtimestamp((message['date'] // 1000)).ctime()))
                    print((BOLD('Subject: ') + fill(message['title'], subsequent_indent=(' ' * 9))))
                    body = message['body'].splitlines()
                    if (len(body) > 0):
                        print((BOLD('Message: ') + body[0]))
                        for line in body[1:]:
                            print(((' ' * 9) + line))
        except Exception as e:
            warn('Error while retrieving greet data: {}'.format(e))
    args.current = False
    args.name = None
    args.level = 'CONTRIBUTE'
    args.public = False
    if ((args.host is not None) and (not args.staging) and (not using_default)):
        setenv(args)
    elif args.projects:
        pick_and_set_project(args)
    if (args.save and (not args.token)):
        msg = 'You are now logged in. Your credentials are stored in {conf_dir} and will expire in {timeout}. {tip}'
        tip = (((('Use ' + BOLD('dx login --timeout')) + ' to control the expiration date, or ') + BOLD('dx logout')) + ' to end this session.')
        timeout = datetime.timedelta(seconds=(normalize_time_input(args.timeout, default_unit='s') // 1000))
        print(fill(msg.format(conf_dir=dxpy.config.get_user_conf_dir(), timeout=timeout, tip=tip)))
