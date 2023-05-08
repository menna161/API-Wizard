import datetime
import json
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from pandas import DataFrame
from .kiwoom import k_module


def details(request, code):
    k_module.set_input_value('종목코드', code)
    k_module.set_input_value('기준일자', datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'))
    k_module.set_input_value('수정주가구분 ', 0)
    k_module.comm_rq_data('주식일봉차트조회요청', 'opt10081', 0, k_module.S_SCREEN_NO)
    data = k_module.qs['OnReceiveTrData'].get()
    daily_stock_data = json.loads(k_module.get_comm_data_ex(data['sTrCode'], data['sRQName']))
    daily_stock_data = DataFrame(daily_stock_data, dtype=int).iloc[:, 1:8]
    daily_stock_data.columns = ['current_price', 'tr_qty', 'tr_volume', 'date', 'start', 'high', 'close']
    daily_stock_data = daily_stock_data.set_index('date')
    k_module.set_input_value('종목코드', code)
    k_module.comm_rq_data('주식기본정보', 'opt10001', 0, k_module.S_SCREEN_NO)
    tr_data = k_module.qs['OnReceiveTrData'].get()
    return render(request, 'kiwoom/details.html', {'login_state': k_module.get_connect_state(), 'name': k_module.comm_get_data(tr_data['sTrCode'], '', tr_data['sRQName'], 0, '종목명'), 'quantity': k_module.comm_get_data(tr_data['sTrCode'], '', tr_data['sRQName'], 0, '거래량'), 'current_price': k_module.comm_get_data(tr_data['sTrCode'], '', tr_data['sRQName'], 0, '현재가'), 'total_price': k_module.comm_get_data(tr_data['sTrCode'], '', tr_data['sRQName'], 0, '시가총액'), 'daily_stock_data': daily_stock_data.to_csv(line_terminator='\\n')})
