import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def test_print_post_text(capsys, monkeypatch):
    '\n    Ensures that proper output when print_post_text is called.\n    '
    path = 'autostack/so_web_scraper/__tests__/data/post_text.html'
    html = open(path).read()
    post_text = BeautifulSoup(html, 'lxml').find(attrs={'class', 'post-text'})

    def mock_other_print_functions(*args):
        '\n        Mocks print_ul and print_code_block functions.\n        '
        return
    monkeypatch.setattr('autostack.so_web_scraper.print_ul', mock_other_print_functions)
    monkeypatch.setattr('autostack.so_web_scraper.print_code_block', mock_other_print_functions)
    print_post_text(post_text)
    captured = capsys.readouterr()
    assert (ANSI_ESCAPE.sub('', captured.out) == (((('Test 1\n' + 'Test 2\n') + 'Test 3\n') + 'Test 4\n') + 'Test 5\n'))
