import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def test_post_soup_accepted_answer(monkeypatch):
    "\n    Ensures that BeautifulSoup is returned when there's an accepted answer.\n    "
    path = 'autostack/so_web_scraper/__tests__/data/post_accepted_answer.html'
    html = open(path).read()
    soup = BeautifulSoup(html, 'lxml')

    def mock_has_accepted_answer(*args):
        '\n        Mocks the has_accepted_answer function.\n        '
        return True

    def mock_get_post_url(*args):
        '\n        Mocks the get_post_url function.\n        '
        return ''
    mock_response = MockResponse(path, 200)
    mock_get = build_mock_get(mock_response)
    monkeypatch.setattr('autostack.so_web_scraper.has_accepted_answer', mock_has_accepted_answer)
    monkeypatch.setattr('autostack.so_web_scraper.get_post_url', mock_get_post_url)
    monkeypatch.setattr('requests.get', mock_get)
    response_soup = post_soup(None)
    assert (response_soup == soup)
