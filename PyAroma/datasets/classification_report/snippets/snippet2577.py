import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def test_has_accepted_answer_true():
    '\n    Ensures that has_accepted_answer returns True when the post\n    does in fact have an accepted answer.\n    '
    html = open('autostack/so_web_scraper/__tests__/data/query_post_summaries.html').read()
    post_summary = BeautifulSoup(html, 'lxml').find_all(attrs={'class': 'question-summary'})[4]
    accepted_answer = has_accepted_answer(post_summary)
    assert accepted_answer
