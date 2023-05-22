import requests
from click.testing import CliRunner
from commandict.get_result import example_url, main, parse, parse_detail, parse_example


def test_parse_detail():
    KEYWORD = 'buy'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    (meanings, wordid) = parse(response.text)
    detailed_url = f'https://dic.daum.net/word/view.do?wordid={wordid}'
    detailed_text = requests.get(detailed_url).text
    result = parse_detail(detailed_text, wordid, 'synonym')
    synonym = 'purchase: 구매하다, 구입하다, 매수하다, 사다, 인수하다\npay for: 대가를 지불하다, 돈을 내다, 내다, 부담하다, 계산하다\nprocure: 조달하다, 입수, 구하다, 도입, 얻다'
    assert (result == synonym)
    result = parse_detail(detailed_text, wordid, 'antonym')
    antonym = 'sell: 팔다, 판매하다, 매각하다, 매도하다, 매매'
    assert (result == antonym)
