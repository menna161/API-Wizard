import requests
from click.testing import CliRunner
from commandict.get_result import example_url, main, parse, parse_detail, parse_example


def test_parse_detail_no_antonym():
    KEYWORD = 'test'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    (meanings, wordid) = parse(response.text)
    detailed_url = f'https://dic.daum.net/word/view.do?wordid={wordid}'
    detailed_text = requests.get(detailed_url).text
    result = parse_detail(detailed_text, wordid, 'synonym')
    synonym = 'work: 일하다, 연구, 작업, 작품, 작동하다\nstudy: 연구, 조사, 공부, 검토하다, 관찰하다\nask: 묻다, 요청하다, 질문하다, 부탁하다, 말씀하다\ngame: 게임, 경기, 시합\nresearch: 연구, 조사, 탐구, 탐사'
    assert (result == synonym)
    result = parse_detail(detailed_text, wordid, 'antonym')
    antonym = 'No results found.'
    assert (result == antonym)
