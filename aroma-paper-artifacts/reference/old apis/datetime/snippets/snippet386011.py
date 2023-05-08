import boto3
import json
import time
import dateutil.parser
import datetime
import calendar


def lambda_handler(event, context):
    processed = False
    DYNAMODB_TABLE = 'DEVOPS_SES_DELIVERIES'
    DDBtable = boto3.resource('dynamodb').Table(DYNAMODB_TABLE)
    SnsMessageId = event['Records'][0]['Sns']['MessageId']
    SnsPublishTime = event['Records'][0]['Sns']['Timestamp']
    SnsTopicArn = event['Records'][0]['Sns']['TopicArn']
    SnsMessage = event['Records'][0]['Sns']['Message']
    print(((('Read SNS Message with ID ' + SnsMessageId) + ' published at ') + SnsPublishTime))
    now = time.strftime('%c')
    LambdaReceiveTime = now
    SESjson = json.loads(SnsMessage)
    sesNotificationType = SESjson['notificationType']
    if ('mail' in SESjson):
        sesMessageId = SESjson['mail']['messageId']
        sesTimestamp = SESjson['mail']['timestamp']
        sender = SESjson['mail']['source']
        print(((('Processing an SES ' + sesNotificationType) + ' with mID ') + sesMessageId))
        if (sesNotificationType == 'Delivery'):
            print('Processing SES delivery message')
            reportingMTA = SESjson['delivery']['reportingMTA']
            deliveryRecipients = SESjson['delivery']['recipients']
            smtpResponse = SESjson['delivery']['smtpResponse']
            deliveryTimestamp = SESjson['delivery']['timestamp']
            processingTime = SESjson['delivery']['processingTimeMillis']
            for recipient in deliveryRecipients:
                recipientEmailAddress = recipient
                print(('Delivery recipient: ' + recipientEmailAddress))
                sesTimestamp_parsed = dateutil.parser.parse(sesTimestamp)
                sesTimestamp_seconds = sesTimestamp_parsed.strftime('%s')
                deliveryTimestamp_parsed = dateutil.parser.parse(deliveryTimestamp)
                deliveryTimestamp_seconds = deliveryTimestamp_parsed.strftime('%s')
                future = (datetime.datetime.utcnow() + datetime.timedelta(days=120))
                expiry_ttl = calendar.timegm(future.timetuple())
                Item = {'recipientAddress': recipientEmailAddress, 'sesMessageId': sesMessageId, 'sesTimestamp': int(sesTimestamp_seconds), 'deliveryTimestamp': int(deliveryTimestamp_seconds), 'processingTime': int(processingTime), 'reportingMTA': reportingMTA, 'smtpResponse': smtpResponse, 'sender': sender.lower(), 'expiry': int(expiry_ttl)}
                response = DDBtable.put_item(Item=Item)
                print('PutItem succeeded:')
                print(json.dumps(response, indent=4, cls=DecimalEncoder))
                processed = True
        else:
            print(('Unhandled notification type: ' + sesNotificationType))
    else:
        print('Incoming event is not a mail event')
        print(('Received event was: ' + json.dumps(event, indent=2)))
        processed = True
    return processed
