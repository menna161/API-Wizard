import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def mock_query_stack_overflow(*args):
    '\n        Mocks the query_stack_overflow function.\n        '
    nonlocal query_stack_overflow_call_count
    query_stack_overflow_call_count += 1
    base = 'autostack/so_web_scraper/__tests__/data/'
    if (query_stack_overflow_call_count == 3):
        return BeautifulSoup(open((base + 'query_no_post_summaries.html')).read(), 'lxml')
    return BeautifulSoup(open((base + 'query_post_summaries.html')).read(), 'lxml')
