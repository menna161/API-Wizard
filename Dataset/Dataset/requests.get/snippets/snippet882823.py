import requests
from click.testing import CliRunner
from commandict.get_result import example_url, main, parse, parse_detail, parse_example


def test_parse_with_polysemy():
    KEYWORD = 'test'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    (meanings, wordid) = parse(response.text)
    assert meanings.startswith('1.시험')
    assert (wordid == 'ekw000167718')
