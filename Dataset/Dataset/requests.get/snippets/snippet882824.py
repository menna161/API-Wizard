import requests
from click.testing import CliRunner
from commandict.get_result import example_url, main, parse, parse_detail, parse_example


def test_parse_no_result():
    KEYWORD = 'cthulhu'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    (result, wordid) = parse(response.text)
    assert (result == 'No results found.')
    assert (wordid == '')
