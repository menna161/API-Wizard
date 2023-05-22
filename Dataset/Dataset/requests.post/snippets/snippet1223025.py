import json
from datetime import datetime
import boto3
import requests


def lambda_handler(event, context):
    client = boto3.client('ce')
    today = datetime.today().strftime('%Y-%m-%d')
    first_day_of_month = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    response = client.get_cost_and_usage(TimePeriod={'Start': first_day_of_month, 'End': today}, Granularity='MONTHLY', Metrics=['AmortizedCost'])
    full_message = (((((((('The total cost for the account *' + ACCOUNT_NAME) + '* from *') + first_day_of_month) + '* up to *') + today) + '* is : _') + response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount']) + '_')
    slack_message_object = {'channel': SLACK_CHANNEL, 'username': USERNAME, 'text': full_message, 'icon_emoji': USER_EMOJI}
    response = requests.post(url=WEBHOOK_URL, data=json.dumps(slack_message_object).encode('utf-8'))
