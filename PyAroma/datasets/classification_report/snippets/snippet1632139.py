from __future__ import print_function
import sys
import subprocess
import base64
import xml.etree.ElementTree as ET
import boto3
from bs4 import BeautifulSoup


def get_temp_credentials(metadata_id, idp_host, ssh_args=None):
    "\n    Use SAML SSO to get a set of credentials that can be used for API access to an AWS account.\n\n    Example:\n      from openshift_tools import saml_aws_creds\n      creds = saml_aws_creds.get_temp_credentials(\n          metadata_id='urn:amazon:webservices:123456789012',\n          idp_host='login.saml.example.com',\n          ssh_args=['-i', '/path/to/id_rsa', '-o', 'StrictHostKeyChecking=no'])\n\n      client = boto3.client(\n          'iam',\n          aws_access_key_id=creds['AccessKeyId'],\n          aws_secret_access_key=creds['SecretAccessKey'],\n          aws_session_token=creds['SessionToken'],\n          )\n    "
    ssh_cmd = ['ssh', '-p', '2222', '-a', '-l', 'user', '-o', 'ProxyCommand=bash -c "exec openssl s_client -servername %h -connect %h:443 -quiet 2>/dev/null \\\n                   < <(echo -en \'CONNECT 127.0.0.1:%p HTTP/1.1\\r\\nHost: %h:443\\r\\n\\r\\n\'; cat -)"']
    if ssh_args:
        ssh_cmd.extend(ssh_args)
    ssh_cmd.extend([idp_host, metadata_id])
    ssh = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (html_saml_assertion, ssh_error) = ssh.communicate()
    if (ssh.returncode != 0):
        raise ValueError(('Error connecting to SAML IdP:\nSTDERR:\n' + ssh_error))
    assertion = None
    soup = BeautifulSoup(html_saml_assertion)
    for inputtag in soup.find_all('input'):
        if (inputtag.get('name') == 'SAMLResponse'):
            assertion = inputtag.get('value')
    if (not assertion):
        error_msg = soup.find('div', {'id': 'content'})
        if error_msg:
            error_msg = error_msg.get_text()
        else:
            error_msg = html_saml_assertion
        raise ValueError(('Error retrieving SAML token: ' + error_msg))
    role = None
    principal = None
    xmlroot = ET.fromstring(base64.b64decode(assertion))
    for saml2attribute in xmlroot.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
        if (saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role'):
            for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                (role, principal) = saml2attributevalue.text.split(',')
    client = boto3.client('sts')
    response = client.assume_role_with_saml(RoleArn=role, PrincipalArn=principal, SAMLAssertion=assertion)
    if (not response['Credentials']):
        raise ValueError('No Credentials returned')
    return response['Credentials']
