import datetime
import uuid
from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.util.WebUtils import *
from alipay.aop.api.util.SignatureUtils import *
from alipay.aop.api.util.CommonUtils import *
from alipay.aop.api.util.EncryptUtils import *


def __prepare_request_params(self, request):
    THREAD_LOCAL.logger = self.__logger
    params = request.get_params()
    if (P_BIZ_CONTENT in params):
        if (self.__config.encrypt_type and self.__config.encrypt_key):
            params[P_BIZ_CONTENT] = encrypt_content(params[P_BIZ_CONTENT], self.__config.encrypt_type, self.__config.encrypt_key, self.__config.charset)
        elif request.need_encrypt:
            raise RequestException((('接口' + params[P_METHOD]) + '必须使用encrypt_type、encrypt_key加密'))
    params[P_TIMESTAMP] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    common_params = self.__get_common_params(params)
    all_params = dict()
    all_params.update(params)
    all_params.update(common_params)
    sign_content = get_sign_content(all_params)
    try:
        if (self.__config.sign_type and (self.__config.sign_type == 'RSA2')):
            sign = sign_with_rsa2(self.__config.app_private_key, sign_content, self.__config.charset)
        else:
            sign = sign_with_rsa(self.__config.app_private_key, sign_content, self.__config.charset)
    except Exception as e:
        raise RequestException(((('[' + THREAD_LOCAL.uuid) + ']request sign failed. ') + str(e)))
    common_params[P_SIGN] = sign
    self.__remove_common_params(params)
    log_url = ((((self.__config.server_url + '?') + sign_content) + '&sign=') + sign)
    if THREAD_LOCAL.logger:
        THREAD_LOCAL.logger.info(((('[' + THREAD_LOCAL.uuid) + ']request:') + log_url))
    return (common_params, params)
