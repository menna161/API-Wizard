import requests
from click.testing import CliRunner
from commandict.get_result import example_url, main, parse, parse_detail, parse_example


def test_parse_example():
    KEYWORD = 'buy'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    (_, wordid) = parse(response.text)
    exp_url = example_url(wordid)
    result = parse_example(exp_url)
    sentence_sample = 'Surprisingly, he has spent about $80,000 to buy the dolls!'
    assert (sentence_sample in result)
