import re
from bs4 import BeautifulSoup
from autostack.so_web_scraper import accepted_posts, get_post_summaries, build_query_url, query_stack_overflow, post_soup, has_accepted_answer, get_post_url, print_accepted_post, get_post_text, print_post_text, print_ul, print_code_block, get_src_code
from autostack.so_web_scraper.__tests__.mock_response import MockResponse, build_mock_get


def test_get_post_url_where_url_exists():
    '\n    Ensures that a url is returned from get_post_url\n    when a url exists.\n    '
    html = open('autostack/so_web_scraper/__tests__/data/query_post_summaries.html').read()
    post_summary = BeautifulSoup(html, 'lxml').find(attrs={'class': 'question-summary'})
    url = get_post_url(post_summary)
    assert (url == '/questions/930397/getting-the-last-element-of-a-list/930398?r=SearchResults#930398')
