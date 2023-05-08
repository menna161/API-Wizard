import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def test_print_ul_populated(capsys):
    '\n    Ensures that all list elements are printed.\n    '
    path = 'autostack/so_web_scraper/__tests__/data/post_text_ul_populated.html'
    html = open(path).read()
    unordered_list = BeautifulSoup(html, 'lxml').find('ul')
    print_ul(unordered_list)
    captured = capsys.readouterr()
    assert (ANSI_ESCAPE.sub('', captured.out) == (('    - Test 1\n' + '    - Test 2\n') + '    - Test 3\n'))