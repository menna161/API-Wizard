import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def test_get_post_text_answer():
    '\n    Ensures the accepted answer post-text is returned for a post.\n    '
    path = 'autostack/so_web_scraper/__tests__/data/post_accepted_answer.html'
    html = open(path).read()
    post = BeautifulSoup(html, 'lxml')
    post_text = get_post_text(post, 'accepted-answer')
    assert post_text
