import json
import sys
import random
import datetime
import time
import requests
import webexteamssdk
from crayons import blue, green, red
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import env_lab
import env_user

if (__name__ == '__main__'):
    webex_username = get_webex_teams_username()
    api_session = requests.Session()
    login_request_data = {'username': SMC_USER, 'password': SMC_PASSWORD}
    login_success = login(api_session, login_request_data)
    if login_success:
        tenants_content = get_tenants(api_session)
        if tenants_content:
            tenant_list = json.loads(tenants_content)['data']
            print(green(f'Found all the following tenants: {tenant_list}'))
            SMC_TENANT_ID = tenant_list[0]['id']
            print(f'Working on Tenant ID is: {SMC_TENANT_ID}')
            time_window = 60
            query_search_id = get_security_events(time_window)
            if query_search_id:
                print(f'''
==> Created query looking for all the hosts that generate high amount of traffic in the last {time_window} minutes.''')
                print('Generating results. Please wait...')
                url = f'https://{SMC_HOST}/sw-reporting/v1/tenants/{SMC_TENANT_ID}/security-events/queries/{query_search_id}'
                percent_complete = 0.0
                while (percent_complete != 100.0):
                    response = api_session.request('GET', url, verify=False)
                    percent_complete = json.loads(response.content)['data']['percentComplete']
                    print(f'Search progress: {percent_complete}%')
                    time.sleep(1)
                print(green(f'Search query completed!'))
                url = f'https://{SMC_HOST}/sw-reporting/v1/tenants/{SMC_TENANT_ID}/security-events/results/{query_search_id}'
                response = api_session.request('GET', url, verify=False)
                results = json.loads(response.content)['data']['results']
                total_security_events = len(results)
                print(f'Total found events: {total_security_events}')
                ip_addresses = set()
                for result in results:
                    source_address = result['source']['ipAddress']
                    ip_addresses.add(source_address)
                    if (len(ip_addresses) == 10):
                        break
                print(f'Collected the following first 10 IP addresses: {ip_addresses}')
                tag_name = f'[{webex_username}] - High Traffic Hosts'
                request_data = [{'name': tag_name, 'location': 'OUTSIDE', 'description': 'Hosts generating or receiving an unusually high amount of traffic.', 'ranges': list(ip_addresses)}]
                id_tag = create_new_tag(request_data)
                if id_tag:
                    print(f'''
==> Sending message to Webex Space bragging for a completed mission! :D''')
                    message = f'''**StealthWatch Enterprise Mission completed!!! :D**
I created the new TAG _{tag_name}_, containing {len(ip_addresses)} IP addresses of hosts generating an unusually high amount of traffic.'''
                    send_webex_message(message)
                    print(green(f'Message sent, StealthWatch Enterprise Mission Completed!!!'))
                    remove_tag(id_tag)
        terminate_session(api_session)
