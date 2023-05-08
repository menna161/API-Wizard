from collections import Counter
from datetime import datetime
import requests
from dateutil.parser import parse


def filter_issue_by_ym(issues):
    filtered_issues = []
    now = datetime.now()
    for issue in issues:
        created_at = parse(issue['created_at'])
        if ((now.year == created_at.year) and (now.month == created_at.month)):
            filtered_issues.append(issue)
    return filtered_issues
