import json
import re
import traceback
import decimal
from atp.httprunner import exceptions, logger, utils, parser
from atp.httprunner.compat import OrderedDict, basestring, is_py2
from requests.models import PreparedRequest
from requests.structures import CaseInsensitiveDict
from atp.api.mysql_sql_executor import sql_execute, db_operation_to_json
from atp.utils.tools import convert_mysql_datatype_to_py


def _extract_field_with_delimiter(self, field, context_obj=None):
    ' response content could be json or html text.\n        @param (str) field should be string joined by delimiter.\n        e.g.\n            "status_code"\n            "headers"\n            "cookies"\n            "content"\n            "headers.content-type"\n            "content.person.name.first_name"\n\n            含用例内变量\n            "123$phoneNo"\n\n            查询SQL\n            "SELECT NEXT_VALUE FROM user_db.sequence WHERE SEQ_NAME=\'$MEMBER_ID\';"\n        '
    sub_str_exp = None
    if (field.endswith(']') and ('[' in field) and (':' in field.split('[')[(- 1)])):
        sub_str_exp = ('[' + field.split('[')[(- 1)])
        field = field.strip(sub_str_exp)
    if str(field).lower().startswith('select '):
        db_connect_content = '$DB_CONNECT'
        parsed_db_connect = context_obj.eval_content(db_connect_content)
        if parser.extract_variables(field):
            sql = context_obj.eval_content(field)
        else:
            sql = field
        from atp.api.mysql_sql_executor import sql_execute, db_operation_to_json
        from atp.utils.tools import convert_mysql_datatype_to_py
        try:
            res = sql_execute(sql, db_connect=parsed_db_connect)
        except Exception as err:
            raise
        if res:
            if (len(res) == 1):
                if (len(res[0]) == 1):
                    res_value = convert_mysql_datatype_to_py(res[0][0])
                else:
                    res_value = db_operation_to_json(sql, db_connect=parsed_db_connect, return_info=res)
            else:
                res_value = []
                for res_item in res:
                    if (len(res_item) == 1):
                        res_value.append(convert_mysql_datatype_to_py(res_item[0]))
                    else:
                        res_value.append(db_operation_to_json(sql, db_connect=parsed_db_connect, return_info=res_item, multi=True))
        else:
            res_value = 'variable sql return no result!'
        return (res_value, sub_str_exp)
    try:
        (top_query, sub_query) = field.split('.', 1)
    except ValueError:
        top_query = field
        sub_query = None
    if (top_query in ['status_code', 'encoding', 'ok', 'reason', 'url']):
        if sub_query:
            err_msg = u'Failed to extract: {}\n'.format(field)
            logger.log_error(err_msg)
            raise exceptions.ParamsError(err_msg)
        return (getattr(self, top_query), sub_str_exp)
    elif (top_query == 'cookies'):
        cookies = self.cookies.get_dict()
        if (not sub_query):
            return (cookies, sub_str_exp)
        try:
            return (cookies[sub_query], sub_str_exp)
        except KeyError:
            err_msg = u'Failed to extract cookie! => {}\n'.format(field)
            err_msg += u'response cookies: {}\n'.format(cookies)
            logger.log_error(err_msg)
            raise exceptions.ExtractFailure(err_msg)
    elif (top_query == 'elapsed'):
        available_attributes = u'available attributes: days, seconds, microseconds, total_seconds'
        if (not sub_query):
            err_msg = u'elapsed is datetime.timedelta instance, attribute should also be specified!\n'
            err_msg += available_attributes
            logger.log_error(err_msg)
            raise exceptions.ParamsError(err_msg)
        elif (sub_query in ['days', 'seconds', 'microseconds']):
            return (getattr(self.elapsed, sub_query), sub_str_exp)
        elif (sub_query == 'total_seconds'):
            return (self.elapsed.total_seconds(), sub_str_exp)
        else:
            err_msg = '{} is not valid datetime.timedelta attribute.\n'.format(sub_query)
            err_msg += available_attributes
            logger.log_error(err_msg)
            raise exceptions.ParamsError(err_msg)
    elif (top_query == 'headers'):
        headers = self.headers
        if (not sub_query):
            return (headers, sub_str_exp)
        try:
            return (headers[sub_query], sub_str_exp)
        except KeyError:
            err_msg = u'Failed to extract header! => {}\n'.format(field)
            err_msg += u'response headers: {}\n'.format(headers)
            logger.log_error(err_msg)
            raise exceptions.ExtractFailure(err_msg)
    elif (top_query in ['content', 'text', 'json']):
        try:
            body = self.json
        except exceptions.JSONDecodeError:
            body = self.text
        if (not sub_query):
            return (body, sub_str_exp)
        if isinstance(body, dict):
            '如果body中content是字符串类型\'content\': "{\'headImageUrl\':\'\',\'isRegister\':0,\'nickName\':\'\'}"\n                  转换成字典，然后\'extract\': [{\'headImageUrl\':"content.content.isRegister"}]可提取\n                '
            if (('content' in body.keys()) and body['content'] and isinstance(body['content'], str)):
                try:
                    body_content_dict = json.loads(body['content'].replace(' style="text-align: center;text-indent: 0;"', '').replace("'", '"'))
                    body['content'] = body_content_dict
                except (TypeError, json.decoder.JSONDecodeError) as e:
                    logger.log_error('\n'.join([e, traceback.format_exc()]))
            return (utils.query_json(body, sub_query), sub_str_exp)
        elif sub_query.isdigit():
            return (utils.query_json(body, sub_query), sub_str_exp)
        else:
            err_msg = u'Failed to extract attribute from response body! => {}\n'.format(field)
            err_msg += u'response body: {}\n'.format(body)
            logger.log_error(err_msg)
            raise exceptions.ExtractFailure(err_msg)
    elif (top_query in self.__dict__):
        attributes = self.__dict__[top_query]
        if (not sub_query):
            return (attributes, sub_str_exp)
        if isinstance(attributes, (dict, list)):
            return (utils.query_json(attributes, sub_query), sub_str_exp)
        elif sub_query.isdigit():
            return (utils.query_json(attributes, sub_query), sub_str_exp)
        else:
            err_msg = u'Failed to extract cumstom set attribute from teardown hooks! => {}\n'.format(field)
            err_msg += u'response set attributes: {}\n'.format(attributes)
            logger.log_error(err_msg)
            raise exceptions.TeardownHooksFailure(err_msg)
    elif (context_obj and parser.extract_variables(top_query)):
        return (context_obj.eval_content(top_query), sub_str_exp)
    else:
        err_msg = u'Failed to extract attribute from response! => {}\n'.format(field)
        err_msg += u'available response attributes: status_code, cookies, elapsed, headers, content, text, json, encoding, ok, reason, url.\n\n'
        err_msg += u'If you want to set attribute in teardown_hooks, take the following example as reference:\n'
        err_msg += u"response.new_attribute = 'new_attribute_value'\n"
        logger.log_error(err_msg)
        raise exceptions.ParamsError(err_msg)
