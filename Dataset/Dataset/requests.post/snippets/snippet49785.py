from github import Github, UnknownObjectException
from flask import render_template
from jinja2 import TemplateNotFound
import requests
from collections import defaultdict


def process_hook(self, pull_request_id, url, args, storage):
    message = self.constants.get('GH_BOT_MESSAGE')
    ci_restart_url = self.constants.get('CI_RESTART_URL')
    ci_api_key = self.constants.get('CI_API_KEY')
    build_id = args.get('build_id')
    if build_id:
        pr = self.repo.get_pull(pull_request_id)
        base_commit_sha = pr.base.sha
        if (not storage.get('master')):
            default = dict(zip(self.languages, self.current))
            default.update({'repo_name': self.repo.name, 'build_id': '1'})
            storage.set('master', {'current': default, 'base_commit_sha': default})
        if (base_commit_sha not in storage.get('master')):
            base_commit_sha = sorted(storage.get('master').items(), key=(lambda x: x[1]['build_id']))[0][0]
        coverage_diffs = self.do_for_each_language((lambda l: (float(args.get(l, 0)) - float(storage.get('master').get(base_commit_sha).get(l)))))
        if (min(coverage_diffs.values()) < (- 10)):
            commit = (self.repo.get_commit(args.get('commit_id')) or pr.get_commits().reversed[0])
            user = (storage.get(commit.author.login) or {'name': commit.author.name, 'login': commit.author.login})
            if (ci_restart_url and (user.get('dangerously_low') != True)):
                user['dangerously_low'] = True
                storage.set(pr.user.login, user)
                url = ci_restart_url.replace('$build_id$', build_id).replace('$api_key$', ci_api_key)
                requests.post(url)
                body = ("Something doesn't look right... I'm re-running the coverage reports." + "This comment will be updated when I'm done.")
                self.post_comment(body, pr)
                return False
    self.update_leaderboard(pull_request_id, args, storage, coverage_diffs)
    self.comment(pull_request_id, message, url, args, storage, coverage_diffs, base_commit_sha)
    return True
