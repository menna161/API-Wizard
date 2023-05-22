import json
import requests
from crayons import blue, green, red
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import env_lab
import env_user

if (__name__ == '__main__'):
    api_session = requests.Session()
    login_request_data = {'username': SMC_USER, 'password': SMC_PASSWORD}
    login_success = login(api_session, login_request_data)
    if login_success:
        tenants_content = get_tenants(api_session)
        if tenants_content:
            tenant_list = json.loads(tenants_content)['data']
            print(green(f'Found the following tenants: {tenant_list}'))
            SMC_TENANT_ID = tenant_list[0]['id']
            print(f'Working on Tenant ID is: {SMC_TENANT_ID}')
            print(f'''
==> Updating the Security Event 16 (Total High Traffic) to meet our needs for the DNE''')
            new_security_event_details = [{'id': 16, 'policyId': 1, 'eventSettings': {'eventStatus': {'sourceStatus': 'ENABLED', 'targetStatus': 'ENABLED'}, 'alarmSettings': [{'key': 'tolerance', 'value': '70'}, {'key': 'min', 'value': '100000'}, {'key': 'max', 'value': '500000'}]}}]
            updated = update_security_event(new_security_event_details)
        terminate_session(api_session)
