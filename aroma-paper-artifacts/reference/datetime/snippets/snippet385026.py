from __future__ import absolute_import, print_function, division
import datetime
import boto3
from monocyte.handler import Resource, Handler


def _fetch_unwanted_resources(self, region_name):
    client = boto3.client('acm', region_name=region_name)
    response = client.list_certificates(CertificateStatuses=['ISSUED'])
    certificate_arns = [summary['CertificateArn'] for summary in response['CertificateSummaryList']]
    limit = (datetime.datetime.now() + datetime.timedelta(days=MIN_VALID_DAYS))
    for certificate_arn in certificate_arns:
        response = client.describe_certificate(CertificateArn=certificate_arn)
        certificate = response['Certificate']
        not_after = datetime.datetime.replace(certificate['NotAfter'], tzinfo=None)
        if (not_after > limit):
            continue
        resource_wrapper = Resource(resource=('Certificate for ' + certificate['DomainName']), resource_type=self.resource_type, resource_id=certificate_arn, creation_date=certificate.get('CreatedAt', certificate.get('ImportedAt')), region='global', reason='will expired soon')
        (yield resource_wrapper)
