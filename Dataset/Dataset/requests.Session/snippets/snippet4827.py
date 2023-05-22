import base64
import hmac
import inspect
import json
import re
import time
from asyncio import Future
from concurrent.futures import ThreadPoolExecutor as Pool
import tornado.httpserver
import tornado.ioloop
import tornado.web
import yaml
from tornado.ioloop import IOLoop
from yieldbreaker import YieldBreaker
from .scopes import Permission
from .utils import ACCEPT_HEADER_SYMMETRA, Authenticator, add_event, clear_caches
import there
import traceback
import requests
import traceback
import traceback
import traceback
import traceback
import traceback


def post(self):
    if self.config.forward_staging_url:
        try:

            def fn(req, url):
                try:
                    import requests
                    headers = {k: req.headers[k] for k in ('content-type', 'User-Agent', 'X-GitHub-Delivery', 'X-GitHub-Event', 'X-Hub-Signature')}
                    req = requests.Request('POST', url, headers=headers, data=req.body)
                    prepared = req.prepare()
                    with requests.Session() as s:
                        res = s.send(prepared)
                    return res
                except Exception:
                    import traceback
                    traceback.print_exc()
            pool.submit(fn, self.request, self.config.forward_staging_url)
        except Exception:
            print((red + 'failure to forward'))
            import traceback
            traceback.print_exc()
    if ('X-Hub-Signature' not in self.request.headers):
        add_event('attack', {'type': 'no X-Hub-Signature'})
        return self.error('WebHook not configured with secret')
    if (not verify_signature(self.request.body, self.request.headers['X-Hub-Signature'], self.config.webhook_secret)):
        add_event('attack', {'type': 'wrong signature'})
        return self.error('Cannot validate GitHub payload with provided WebHook secret')
    payload = tornado.escape.json_decode(self.request.body)
    org = payload.get('repository', {}).get('owner', {}).get('login')
    if (not org):
        org = payload.get('issue', {}).get('repository', {}).get('owner', {}).get('login')
        print('org in issue', org)
    if (payload.get('action', None) in ['edited', 'assigned', 'labeled', 'opened', 'created', 'submitted']):
        add_event('ignore_org_missing', {'edited': 'reason'})
    elif (hasattr(self.config, 'org_allowlist') and (org not in self.config.org_allowlist)):
        add_event('post', {'reject_organisation': org})
    sender = payload.get('sender', {}).get('login', {})
    if (hasattr(self.config, 'user_denylist') and (sender in self.config.user_denylist)):
        add_event('post', {'blocked_user': sender})
        self.finish('Blocked user.')
        return
    action = payload.get('action', None)
    add_event('post', {'accepted_action': action})
    unknown_repo = ((red + '<unknown repo>') + normal)
    repo = payload.get('repository', {}).get('full_name', unknown_repo)
    if (repo == unknown_repo):
        import there
        there.print(json.dumps(payload))
    if payload.get('commits'):
        etype = self.request.headers.get('X-GitHub-Event')
        num = payload.get('size')
        ref = payload.get('ref')
        by = payload.get('pusher', {}).get('name')
        print((green + f'(https://github.com/{repo}) `{num}` commit(s) were pushed to `{ref}` by `{by}` – type: {etype}'))
        self.finish('commits were pushed to {repo}')
        return
    if action:
        return self.dispatch_action(action, payload)
    else:
        event_type = self.request.headers.get('X-GitHub-Event')
        if (event_type == 'pull_request'):
            return self.finish()
        if (event_type in {'status', 'fork', 'deployment_status', 'deployment', 'delete', 'push', 'create'}):
            print(f'(https://github.com/{repo}) Not handling event type `{event_type}` yet.')
            return self.finish()
        print(f'({repo}) No action available for the webhook :', event_type)
