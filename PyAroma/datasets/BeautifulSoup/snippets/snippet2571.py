import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def test_query_stack_overflow_good_response_status(monkeypatch):
    '\n    Ensures that BeautifulSoup is returned from query_stack_overflow.\n    '
    path = 'autostack/so_web_scraper/__tests__/data/query_post_summaries.html'
    html = open(path).read()
    soup = BeautifulSoup(html, 'lxml')
    mock_response = MockResponse(path, 200)
    mock_get = build_mock_get(mock_response)
    monkeypatch.setattr('requests.get', mock_get)
    response = query_stack_overflow(None)
    assert (response == soup)
