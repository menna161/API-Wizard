import json
import os
import datetime
import time
import boto3
import botocore


def evaluate_compliance(event, context, configuration_item, valid_rule_parameters):
    'Form the evaluation(s) to be return to Config Rules\n\n    Return either:\n    None -- when no result needs to be displayed\n    a string -- either COMPLIANT, NON_COMPLIANT or NOT_APPLICABLE\n    a dictionary -- the evaluation dictionary, usually built by build_evaluation_from_config_item()\n    a list of dictionary -- a list of evaluation dictionary , usually built by build_evaluation()\n\n    Keyword arguments:\n    event -- the event variable given in the lambda handler\n    configuration_item -- the configurationItem dictionary in the invokingEvent\n    valid_rule_parameters -- the output of the evaluate_parameters() representing validated parameters of the Config Rule\n\n    Advanced Notes:\n    1 -- if a resource is deleted and generate a configuration change with ResourceDeleted status, the Boilerplate code will put a NOT_APPLICABLE on this resource automatically.\n    2 -- if a None or a list of dictionary is returned, the old evaluation(s) which are not returned in the new evaluation list are returned as NOT_APPLICABLE by the Boilerplate code\n    3 -- if None or an empty string, list or dict is returned, the Boilerplate code will put a "shadow" evaluation to feedback that the evaluation took place properly\n    '
    compliance_account_id = context.invoked_function_arn.split(':')[4]
    compliance_account_region = context.invoked_function_arn.split(':')[3]
    compliance_account_partition = context.invoked_function_arn.split(':')[1]
    TEMPLATE_BUCKET = '-'.join([BUCKET_PREFIX, compliance_account_id, compliance_account_region])
    invoking_account_id = event['accountId']
    template = {}
    json_name = (invoking_account_id + '.json')
    role_arn_codepipeline = ((('arn:aws:iam::' + compliance_account_id) + ':role/') + ROLE_NAME_CODEPIPELINE)
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(TEMPLATE_BUCKET, json_name)
        try:
            template = json.loads(obj.get()['Body'].read().decode('utf-8'))
        except Exception as e:
            if ('Expecting value: line 1 column 1 (char 0)' in str(e)):
                obj_default = s3.Object(TEMPLATE_BUCKET, DEFAULT_TEMPLATE)
                template = json.loads(obj_default.get()['Body'].read().decode('utf-8'))
            else:
                raise
    except Exception as e:
        s3_compliance = get_client_from_role('s3', role_arn_codepipeline)
        empty_json = s3_compliance.put_object(Bucket=TEMPLATE_BUCKET, Key=json_name)
        try:
            cp_compliance = get_client_from_role('codepipeline', role_arn_codepipeline, os.environ['MainRegion'])
        except:
            cp_compliance = get_client_from_role('codepipeline', role_arn_codepipeline)
        exec_pipeline = cp_compliance.start_pipeline_execution(name=CODEPIPELINE_NAME)
        return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation='Unable to load most recent template from S3. Auto-deployment has been triggered.')
    config_rule_list = {}
    try:
        config_rule_list = get_all_rules()
    except Exception as e:
        return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation='Unable to get status of Config Rules.')
    template_rules_detail = []
    for (k, resource) in template['Resources'].items():
        if (resource['Type'] == 'AWS::Config::ConfigRule'):
            rule_found = False
            for rule in config_rule_list:
                if (rule['ConfigRuleName'] == resource['Properties']['ConfigRuleName']):
                    template_rules_detail.append(rule)
                    rule_found = True
                    if ('Scope' in resource['Properties']):
                        if ('Scope' not in rule):
                            return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation=(('The rule (' + rule['ConfigRuleName']) + ") has an incorrect 'Scope' configuration."))
                        if (resource['Properties']['Scope'] != rule['Scope']):
                            return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation=(('The rule (' + rule['ConfigRuleName']) + ") has an incorrect 'Scope' configuration."))
                    if ('Source' in resource['Properties']):
                        if ('Source' not in rule):
                            return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation=(('The rule (' + rule['ConfigRuleName']) + ") has an incorrect 'Source' configuration."))
                        if (resource['Properties']['Source']['Owner'] != rule['Source']['Owner']):
                            return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation=(('The rule (' + rule['ConfigRuleName']) + ") has an incorrect 'Owner' configuration."))
                        if ('SourceDetails' in resource['Properties']['Source']):
                            if ('SourceDetails' not in rule['Source']):
                                return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation=(('The rule (' + rule['ConfigRuleName']) + ") has an incorrect 'Source' configuration."))
                            if (resource['Properties']['Source']['SourceDetails'] != rule['Source']['SourceDetails']):
                                return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation=(('The rule (' + rule['ConfigRuleName']) + ") has an incorrect 'Source' configuration."))
                        if ('Fn::Sub' in resource['Properties']['Source']['SourceIdentifier']):
                            resource_lambda = resource['Properties']['Source']['SourceIdentifier']['Fn::Sub'].replace('${AWS::Partition}', compliance_account_partition).replace('${AWS::Region}', compliance_account_region).replace('${LambdaAccountId}', compliance_account_id)
                        else:
                            resource_lambda = resource['Properties']['Source']['SourceIdentifier']
                        if (resource_lambda != rule['Source']['SourceIdentifier']):
                            return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation=(('The rule (' + rule['ConfigRuleName']) + ") has an incorrect 'SourceIdentifier' configuration."))
                    if (rule['ConfigRuleState'] != 'ACTIVE'):
                        return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation=(('The rule (' + rule['ConfigRuleName']) + ') is not active.'))
            if (not rule_found):
                return build_evaluation(invoking_account_id, 'NON_COMPLIANT', event, annotation=(('The rule (' + resource['Properties']['ConfigRuleName']) + ') is not deployed.'))
    try:
        kinesis_client = get_client_from_role('firehose', role_arn_codepipeline, os.environ['MainRegion'])
    except:
        kinesis_client = get_client_from_role('firehose', role_arn_codepipeline)
    for rule in template_rules_detail:
        rule_evaluations = get_all_compliance_evaluations(rule['ConfigRuleName'])
        time.sleep(1)
        for result_id in rule_evaluations:
            json_result = {'ConfigRuleArn': rule['ConfigRuleArn'], 'EngineRecordedTime': str(datetime.datetime.now()).split('.')[0].split('+')[0], 'ConfigRuleName': rule['ConfigRuleName'], 'ResourceType': result_id['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceType'], 'ResourceId': result_id['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId'], 'ComplianceType': result_id['ComplianceType'], 'ResultRecordedTime': str(result_id['ResultRecordedTime']).split('.')[0].split('+')[0], 'ConfigRuleInvokedTime': str(result_id['ConfigRuleInvokedTime']).split('.')[0].split('+')[0], 'AccountId': invoking_account_id, 'AwsRegion': rule['ConfigRuleArn'].split(':')[3]}
            if ('Annotation' in result_id):
                json_result['Annotation'] = result_id['Annotation']
            else:
                json_result['Annotation'] = 'None'
            kinesis_client.put_record(DeliveryStreamName=FIREHOSE_NAME, Record={'Data': json.dumps(json_result)})
    return 'COMPLIANT'
