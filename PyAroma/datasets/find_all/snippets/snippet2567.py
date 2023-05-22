import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def test_accepted_posts(monkeypatch):
    '\n    Ensures that accepted_posts loops over each post summary.\n    '
    post_soup_call_count = 0

    def mock_get_post_summaries(*args):
        '\n        Mocks the get_post_summaries function\n        '
        html = open('autostack/so_web_scraper/__tests__/data/query_post_summaries.html').read()
        post_summaries = BeautifulSoup(html, 'lxml').find_all(attrs={'class': 'question-summary'})
        return [post_summaries]

    def mock_post_soup(*args):
        '\n        Mocks the post_soup function\n        '
        nonlocal post_soup_call_count
        post_soup_call_count += 1
        return 'SOUP'
    monkeypatch.setattr('autostack.so_web_scraper.get_post_summaries', mock_get_post_summaries)
    monkeypatch.setattr('autostack.so_web_scraper.post_soup', mock_post_soup)
    for post in accepted_posts(None):
        pass
    assert (post_soup_call_count == 15)
