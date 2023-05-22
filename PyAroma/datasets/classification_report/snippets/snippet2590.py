import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def test_get_src_code():
    '\n    Ensures that all source code is returned.\n    '
    line_1 = 'l = [[1, 2, 3], [4, 5, 6], [7], [8, 9]]\n'
    line_2 = 'reduce(lambda x, y: x.extend(y), l)'
    path = 'autostack/so_web_scraper/__tests__/data/post_text_code.html'
    html = open(path).read()
    code_block = BeautifulSoup(html, 'lxml').find('div').find('code')
    src_code = get_src_code(code_block)
    assert (src_code == (line_1 + line_2))
