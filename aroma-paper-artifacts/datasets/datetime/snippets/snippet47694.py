import os.path
import sys
import json
import fcntl
import shutil
import gettext
from datetime import datetime
import zipfile
from acm import ACMClient, DEFAULT_GROUP_NAME
import argparse
import traceback


def add(args):
    if (':' in args.namespace):
        pos = args.namespace.index(':')
        e = args.namespace[:pos]
        ns = args.namespace[(pos + 1):]
    else:
        e = DEFAULT_ENDPOINT
        ns = args.namespace
    config = read_config()
    alias = (args.alias or ns)
    if ((args.alias is not None) and (':' in args.alias)):
        print('":" is invalid symbol in alias.')
        sys.exit(1)
    for (ep, ep_info) in config['endpoints'].items():
        for (k, v) in ep_info['namespaces'].items():
            if ((args.alias is None) and (v['alias'] == alias) and ((k != ns) or (ep != e))):
                alias = '-'.join([e, ns])
            elif ((v['alias'] == alias) and (k != ns)):
                print(('Alias %s has been taken by %s:%s, choose another one.' % (_colored(alias, 'red'), ep, k)))
                sys.exit(1)
    if (e not in config['endpoints']):
        if args.kms:
            if (not args.region_id):
                print((_colored('Region ID', 'red') + ' must be specified to use KMS.'))
                sys.exit(1)
        config['endpoints'][e] = {'tls': args.tls, 'is_current': False, 'region_id': args.region_id, 'kms_enabled': args.kms, 'namespaces': {}}
        print(('Adding a new endpoint: %s, using TLS is %s.\n' % (_colored(e, 'yellow'), _colored(args.tls, 'yellow'))))
    else:
        endpoint = config['endpoints'][e]
        if (args.kms and (not args.region_id) and (not endpoint.get('region_id'))):
            print((_colored('Region ID', 'red') + ' must be specified to use KMS.'))
            sys.exit(1)
        if (endpoint.get('tls') != args.tls):
            endpoint['tls'] = args.tls
            print(('TLS attr of %s has changed to %s.\n' % (_colored(e, 'yellow'), _colored(args.tls, 'yellow'))))
        if (endpoint.get('kms_enabled') != args.kms):
            endpoint['kms_enabled'] = args.kms
            print(('KMS enabled of %s has turned to %s.\n' % (_colored(e, 'yellow'), _colored(args.kms, 'yellow'))))
        if (args.region_id is not None):
            if (endpoint.get('region_id') != args.region_id):
                endpoint['region_id'] = args.region_id
                print(('Region ID of %s has changed to %s.\n' % (_colored(e, 'yellow'), _colored(args.region_id, 'yellow'))))
    if (ns in config['endpoints'][e]['namespaces']):
        namespace = config['endpoints'][e]['namespaces'][ns]
        if (args.ak is not None):
            namespace['ak'] = args.ak
        if (args.sk is not None):
            namespace['sk'] = args.sk
        if (args.alias is not None):
            namespace['alias'] = alias
        if (args.kms_ak is not None):
            namespace['kms_ak'] = args.kms_ak
        if (args.kms_secret is not None):
            namespace['kms_secret'] = args.kms_secret
        if (args.key_id is not None):
            namespace['key_id'] = args.key_id
        if (args.ram_role_name is not None):
            namespace['ram_role_name'] = args.ram_role_name
        if args.kms:
            if (not namespace.get('kms_ak')):
                if ((not namespace.get('ak')) and (not namespace['ram_role_name'])):
                    print((((_colored('AccessKey', 'red') + ' or ') + _colored('RAM role name', 'red')) + ' must be specified to use KMS.'))
                    sys.exit(1)
                namespace['kms_ak'] = namespace.get('ak')
            if ((not namespace.get('kms_secret')) and (not namespace['ram_role_name'])):
                if (not namespace.get('sk')):
                    print((((_colored('SecretKey', 'red') + ' or ') + _colored('RAM role name', 'red')) + ' must be specified to use KMS.'))
                    sys.exit(1)
                namespace['kms_secret'] = namespace.get('sk')
        namespace['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(('Namespace %s is already exist in %s, updating configs.\n' % (_colored(ns, 'green'), _colored(e, 'yellow'))))
    else:
        namespace = {'ak': args.ak, 'sk': args.sk, 'alias': alias, 'is_current': False, 'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'kms_ak': None, 'kms_secret': None, 'key_id': None, 'ram_role_name': args.ram_role_name}
        if args.kms:
            kms_ak = (args.kms_ak or args.ak)
            if ((not kms_ak) and (not args.ram_role_name)):
                print((((_colored('AccessKey', 'red') + ' or ') + _colored('RAM role name', 'red')) + ' must be specified to use KMS.'))
                sys.exit(1)
            kms_secret = (args.kms_secret or args.sk)
            if ((not kms_secret) and (not args.ram_role_name)):
                print((((_colored('SecretKey', 'red') + ' or ') + _colored('RAM role name', 'red')) + ' must be specified to use KMS.'))
                sys.exit(1)
            namespace['kms_ak'] = kms_ak
            namespace['kms_secret'] = kms_secret
            namespace['key_id'] = args.key_id
        config['endpoints'][e]['namespaces'][ns] = namespace
        print(('Add new namespace %s(%s) to %s.\n' % (_colored(ns, 'green'), _colored(alias, 'green'), _colored(e, 'yellow'))))
    write_config(config)
    try:
        print('Try to access the namespace...')
        c = ACMClient(endpoint=e, namespace=(None if (ns == '[default]') else ns), ak=config['endpoints'][e]['namespaces'][ns]['ak'], sk=config['endpoints'][e]['namespaces'][ns]['sk'], ram_role_name=config['endpoints'][e]['namespaces'][ns].get('ram_role_name'))
        if config['endpoints'][e]['tls']:
            c.set_options(tls_enabled=True)
        c.list(1, 1)
        print('Namespace access succeed.')
    except:
        print(_colored('\nWarning: Access test failed, there may be mistakes in configuration.\n', 'grey'))
