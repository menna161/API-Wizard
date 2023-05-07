from datetime import datetime, timedelta
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set
from github import Github
from github.Issue import Issue
from github.IssueComment import IssueComment
from github.IssueEvent import IssueEvent
from pydantic import BaseModel, BaseSettings, SecretStr, validator


def process_issue(*, issue: Issue, settings: Settings) -> None:
    logging.info(f'Processing issue: #{issue.number}')
    label_strs = set([label.name for label in issue.get_labels()])
    events = list(issue.get_events())
    labeled_events = get_labeled_events(events)
    last_comment = get_last_comment(issue)
    for (keyword, keyword_meta) in settings.input_config.items():
        closable_delay = ((last_comment is None) or ((datetime.utcnow() - keyword_meta.delay) > last_comment.created_at))
        if (keyword in label_strs):
            logging.info(f'Keyword: "{keyword}" in issue labels')
            keyword_event = get_last_event_for_label(labeled_events=labeled_events, label=keyword)
            if (last_comment and keyword_event and (last_comment.created_at > keyword_event.created_at)):
                logging.info(f'Not closing as the last comment was written after adding the label: "{keyword}"')
                if keyword_meta.remove_label_on_comment:
                    logging.info(f'Removing label: "{keyword}"')
                    issue.remove_from_labels(keyword)
            elif closable_delay:
                close_issue(issue=issue, keyword_meta=keyword_meta, keyword=keyword, label_strs=label_strs)
                break
            else:
                logging.info(f"Not clossing issue: #{issue.number} as the delay hasn't been reached: {keyword_meta.delay}")
