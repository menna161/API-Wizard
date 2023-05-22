from sys import argv
from .config import get_lambda_addr
from .splash_utils import parse_result_and_output
from .general_utils import ACTION, CMD_ACTION
import requests
import json
from base64 import b64decode


def send_command(args, lambda_addr):
    "\n    *\n    * @Purpose:  Sends a command to the LEX (Lambda Executor) to execute.\n    * @Params: args        -> list of form [cmd, arg1, arg2, ... argN]\n    *          lambda_addr -> address of lambda\n    *\n    * @Returns: result -> LEXResult Enum\n    *           output -> result data (For LEXResult.OK this is the command's output)\n    *\n    "
    post_data = {ACTION: CMD_ACTION, CMD_ACTION: args}
    response = requests.post(lambda_addr, json=post_data)
    if (not response):
        raise Exception("[+] Didn't get response from lambda at {}".format(lambda_addr))
    decoded_response = response.content.decode('utf8')
    try:
        resp_json = json.loads(decoded_response)
    except json.decoder.JSONDecodeError as e:
        raise Exception("[!] send_command: Lambda response body isn't JSON decodeable") from e
    (result, output_b64) = parse_result_and_output(resp_json, 'send_command')
    output = b64decode(bytes(output_b64, 'ascii'))
    try:
        output = output.decode('utf8')
    except UnicodeDecodeError:
        pass
    return (result, output)
