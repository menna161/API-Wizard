import requests
from click.testing import CliRunner
from commandict.get_result import example_url, main, parse, parse_detail, parse_example


def test_parse_no_polysemy():
    KEYWORD = 'buy'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    (meanings, wordid) = parse(response.text)
    assert meanings.startswith('1.사다')
    assert (wordid == 'ekw000024208')
