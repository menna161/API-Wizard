import time
from datetime import datetime
from queue import Queue
from qdata.tianyancha.company_filter_options import get_category_data, get_area_data, get_reg_status, get_capital_unit, get_company_type, get_institution_type, get_financing_round, get_listed_type
from qdata.tianyancha import get_company_count
from qdata.errors import QdataError


def test_get_company_count_2():
    '\n    查询\n    <地区>在山东和河南\n    <行业>为采矿业\n    <注册资本>在5000万以上\n    <成立时间>5年前成立的\n    <公司类型>有限责任公司\n    <有无联系方式>有\n    的公司个数\n    '
    count = get_company_count(area_code=['370000', '410000'], category=['B'], reg_capital_range=[(5000, (- 1))], establish_time_range=[((- 1), int((datetime.now().replace((datetime.now().year - 5)).timestamp() * 1000)))], company_type=['有限责任公司'], has_phone=True)
    print(count)
