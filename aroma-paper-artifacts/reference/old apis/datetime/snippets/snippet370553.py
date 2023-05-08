import json
import re
from datetime import datetime
from atp.api.mysql_manager import ApiTestcaseInfoManager, ApiIntfInfoManager, ApiTestcaseRequestManager, ApiPublicVariableInfoManager, ApiSystemInfoManager, ApiTestcaseSubManager, ApiTestcaseMainManager, ApiTestcaseTagRelationManager, ApiTestcaseMainTagRelationManager, ApiTestcaseMainCustomFlowManager
from atp.engine.code_to_desc import get_case_type_by_desc
from atp.utils.common import read_custom
from atp.engine.exceptions import RunCaseError, LoadCaseError
from atp.utils.map_functions import map_testcase_type_to_number
from atp.utils.tools import json_dumps, json_loads
from atp.api.comm_log import logger


def handle_api_testcase(action, **kwargs):
    '\n    新版-保存测试用例到数据库\n    :param action:\n    :param kwargs:\n    :return:\n    '
    base = kwargs.pop('base')
    testcase_name = base.pop('testcaseName')[:200]
    simple_desc = base.pop('testcaseDesc', '')[:1000]
    expect_result = base.pop('expectResult')[:200]
    intf_id = base.pop('intfId')
    operator = kwargs.pop('userName')
    tag_id_list = base.pop('tagIdList')
    intf_obj = ApiIntfInfoManager.get_intf(id=intf_id)
    intf_type = intf_obj.intf_type
    testcase_type = map_testcase_type_to_number(intf_type)
    hr_request = {'name': testcase_name, 'config': {'variables': [], 'request': {'base_url': ''}}, 'teststeps': []}
    setup_cases = kwargs.pop('setupCases', [])
    setup_cases_list = []
    for setup_case_dic in setup_cases:
        case_type_code = get_case_type_by_desc(setup_case_dic['caseType'])
        if (case_type_code == 1):
            setup_case_str = '{0}-{1}'.format(case_type_code, setup_case_dic['testcaseId'])
            if (not setup_case_dic['hasChildren']):
                setup_case_str += '-self'
            setup_cases_list.append(setup_case_str)
        elif (case_type_code == 2):
            setup_case_str = '{0}-{1}'.format(case_type_code, setup_case_dic['testcaseId'])
            flow_id = setup_case_dic.get('customFlowId', None)
            if flow_id:
                setup_case_str += '-{0}'.format(flow_id)
            setup_cases_list.append(setup_case_str)
    steps = kwargs.pop('steps')
    step_no = 0
    empty_check_param_list = None
    for step in steps:
        step_no += 1
        setup_info = step.pop('setupInfo')
        variable_info = step.pop('variableInfo')
        request_info = step.pop('requestInfo')
        validate_info = step.pop('validateInfo')
        extract_info = step.pop('extractInfo')
        teardown_info = step.pop('teardownInfo')
        request_teardown_info = step.pop('requestTeardownInfo', [])
        testcase = {'name': '{testcase}.{step}'.format(testcase=testcase_name, step=step_no), 'variables': [], 'request': {}, 'validate': [], 'extract': [], 'setup_hooks': [], 'teardown_hooks': [], 'request_teardown_hooks': []}
        for variable in variable_info:
            if (variable['type'] == 'function'):
                func_args = ''
                input_args_dic = variable['args']
                for custom_func in CUSTOM['functions']:
                    if (custom_func['name'] == variable['value']):
                        for x in custom_func['parameters']:
                            for input_arg in input_args_dic:
                                if (input_arg == x):
                                    if (func_args == ''):
                                        func_args += input_args_dic[input_arg]
                                    else:
                                        func_args += '||{}'.format(input_args_dic[input_arg])
                testcase['variables'].append({variable['name'].strip(): '${{{func}({args})}}'.format(func=variable['value'], args=func_args)})
            elif (variable['type'] == 'db'):
                '\n                从\n                {\n                    "type": "db",\n                    "name": "next_member_id",\n                    "value": "SELECT NEXT_VALUE FROM user_db.sequence WHERE SEQ_NAME=\'MEMBER_ID\';",\n                    "args": {}\n                }\n                变换成\n                {\n                    \'V_SQL_next_member_id\': "SELECT NEXT_VALUE FROM user_db.sequence WHERE SEQ_NAME=\'MEMBER_ID\';"\n                },\n                {\n                    \'next_member_id\': \'${variable_db_operation(V_SQL_next_member_id||$DB_CONNECT)}\'\n                },\n                '
                sql = variable['value']
                default_func = 'variable_db_operation'
                testcase['variables'].append({variable['name'].strip(): '${{{func}({sql}||$DB_CONNECT)}}'.format(func=default_func, sql=sql)})
            else:
                actual_var_value = transfer_to_actual_value(variable)
                testcase['variables'].append({variable['name'].strip(): actual_var_value})
        for validate in validate_info:
            testcase['validate'].append({validate['comparator']: [validate['check'].strip('\n').strip(), validate['expect'], validate['comment']]})
        for extract in extract_info:
            testcase['extract'].append({extract['saveAs'].strip(): extract['check']})
        case_step_count = 0
        for setup in setup_info:
            '添加前置步骤：执行用例\n             ******teststeps[]字典列表中，最后一个字典为当前用例，'
            for setup_hook in CUSTOM['setup-hooks']:
                if (setup_hook['name'] == setup['name']):
                    if (setup['name'] == 'setup_server_upload_file'):
                        setup_cell = '${{setup_server_upload_file({0}||{1}||{2})}}'.format(setup['args']['ssh_connect'], setup['args']['local_path'].replace('\\', '/'), setup['args']['remote_path'].replace('\\', '/'))
                    else:
                        if isinstance(setup['args'], dict):
                            func_args = ''
                            for base_key in setup_hook['parameters']:
                                for (key, value) in setup['args'].items():
                                    if (key == base_key):
                                        if (func_args == ''):
                                            func_args += value
                                        else:
                                            func_args += '||{}'.format(value)
                        elif isinstance(setup['args'], list):
                            func_args = '||'.join(setup['args'])
                        else:
                            func_args = setup['args']
                        setup_cell = '${{{func_name}({func_args})}}'.format(func_name=setup['name'], func_args=func_args)
                    testcase['setup_hooks'].append(setup_cell)
        for teardown in teardown_info:
            for teardown_hook in CUSTOM['teardown-hooks']:
                if (teardown_hook['name'] == teardown['name']):
                    if isinstance(teardown['args'], dict):
                        func_args = ''
                        for base_key in teardown_hook['parameters']:
                            for (key, value) in teardown['args'].items():
                                if (key == base_key):
                                    if (func_args == ''):
                                        func_args += value
                                    else:
                                        func_args += '||{}'.format(value)
                    elif isinstance(teardown['args'], list):
                        func_args = '||'.join(teardown['args'])
                    else:
                        func_args = teardown['args']
                    teardown_cell = '${{{func_name}({func_args})}}'.format(func_name=teardown['name'], func_args=func_args)
                    testcase['teardown_hooks'].append(teardown_cell)
        for teardown in request_teardown_info:
            for teardown_hook in CUSTOM['teardown-hooks']:
                if (teardown_hook['name'] == teardown['name']):
                    if isinstance(teardown['args'], dict):
                        args_list = []
                        for base_key in teardown_hook['parameters']:
                            for (key, value) in teardown['args'].items():
                                if (key == base_key):
                                    args_list.append(value)
                                    break
                        func_args = '||'.join(args_list)
                    elif isinstance(teardown['args'], list):
                        func_args = '||'.join(teardown['args'])
                    else:
                        func_args = teardown['args']
                    teardown_cell = '${{{func_name}({func_args})}}'.format(func_name=teardown['name'], func_args=func_args)
                    testcase['request_teardown_hooks'].append(teardown_cell)
        is_merge = request_info.pop('isMerge', None)
        testcase['request']['isMerge'] = (True if is_merge else False)
        if (intf_type == 'HTTP'):
            json_body = request_info.pop('json', None)
            sign_func = request_info.pop('sign', None)
            empty_check_param_list = request_info.pop('emptyCheckParamList', None)
            if (json_body is not None):
                testcase['request']['json'] = json_body
            if sign_func:
                for setup_hook in CUSTOM['sign']:
                    if (setup_hook['name'] == sign_func):
                        testcase['setup_hooks'].append('${{{sign_func}($request||$REMOTE_HOST)}}'.format(sign_func=sign_func))
        elif (intf_type == 'DUBBO'):
            testcase['request']['json'] = {'args': []}
            dubbo_args = request_info.pop('args', None)
            if (dubbo_args is not None):
                if isinstance(dubbo_args, list):
                    testcase['request']['json']['args'] = dubbo_args
                else:
                    testcase['request']['json']['args'].append(dubbo_args)
        elif (intf_type == 'MQ'):
            testcase['request']['json'] = {'msg': '{}'}
            mq_msg = request_info.pop('msg', None)
            if (mq_msg is not None):
                testcase['request']['json']['msg'] = mq_msg
        hr_request['teststeps'].append(testcase)
    include = kwargs.pop('include')
    if ((not isinstance(include, list)) or (include == [])):
        include = [{'public_variables': []}]
    '加载public_variables'
    intf_variables = re.findall(variable_regexp, str(intf_obj.intf_info))
    case_variables = re.findall(variable_regexp, str(testcase))
    case_variables.extend(intf_variables)
    target_pv_name_list = list(set(case_variables).difference(set(env_variable_list)))
    for target_pv_name in target_pv_name_list:
        system_id = intf_obj.api_system_id
        s_var_obj = ApiPublicVariableInfoManager.get_variable(variable_name=target_pv_name, api_system_id=system_id)
        if s_var_obj:
            if (s_var_obj.id not in include[0]['public_variables']):
                include[0]['public_variables'].append(s_var_obj.id)
        else:
            company_id = ApiSystemInfoManager.get_system(id=system_id).api_company_id
            c_var_obj = ApiPublicVariableInfoManager.get_variable(variable_name=target_pv_name, api_company_id=company_id)
            if (c_var_obj and (c_var_obj.id not in include[0]['public_variables'])):
                include[0]['public_variables'].append(c_var_obj.id)
    '保存必填字段校验'
    if empty_check_param_list:
        include.append({'param_check': {'empty': empty_check_param_list}})
    if (action == 'add'):
        ApiTestcaseInfoManager.insert_testcase(testcase_name=testcase_name, type=testcase_type, include=json_dumps(include), simple_desc=simple_desc, case_status=0, api_intf_id=intf_id, creator=operator, last_modifier=operator, expect_result=expect_result, setup_case_list=json_dumps(setup_cases_list), last_modify_time=datetime.now())
        tc_objs = ApiTestcaseInfoManager.get_testcases_order_by_create_time_desc(api_intf_id=intf_id, testcase_name=testcase_name, creator=operator, expect_result=expect_result)
        if (not tc_objs):
            logger.error('tc_objs not found')
            raise LoadCaseError
        else:
            testcase_id = tc_objs[0].id
        ApiTestcaseRequestManager.insert_request(api_testcase_id=testcase_id, request=json_dumps(hr_request))
        set_testcase_tag(testcase_id, tag_id_list)
    elif (action == 'edit'):
        testcase_id = base.pop('testcaseId')
        ApiTestcaseInfoManager.update_testcase(id_=testcase_id, testcase_name=testcase_name, include=json_dumps(include), simple_desc=simple_desc, last_modifier=operator, expect_result=expect_result, setup_case_list=json_dumps(setup_cases_list), last_modify_time=datetime.now())
        r_obj = ApiTestcaseRequestManager.get_request(api_testcase_id=testcase_id)
        ApiTestcaseRequestManager.update_request(id_=r_obj.id, request=json_dumps(hr_request))
        set_testcase_tag(testcase_id, tag_id_list)
