import sys
from abc import ABC, abstractmethod
from datetime import datetime
import requests
from persistence import BookmarkDatabase


def execute(self, data):
    bookmarks_imported = 0
    github_username = data['github_username']
    next_page_of_results = f'https://api.github.com/users/{github_username}/starred'
    while next_page_of_results:
        stars_response = requests.get(next_page_of_results, headers={'Accept': 'application/vnd.github.v3.star+json'})
        next_page_of_results = stars_response.links.get('next', {}).get('url')
        for repo_info in stars_response.json():
            repo = repo_info['repo']
            if data['preserve_timestamps']:
                timestamp = datetime.strptime(repo_info['starred_at'], '%Y-%m-%dT%H:%M:%SZ')
            else:
                timestamp = None
            bookmarks_imported += 1
            AddBookmarkCommand().execute(self._extract_bookmark_info(repo), timestamp=timestamp)
    return (True, bookmarks_imported)
