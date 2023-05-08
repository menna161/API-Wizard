import requests
import json
import re
import pytz
import datetime
import time
from dao.redis_dao import predict_insert_
from sklearn.linear_model import LinearRegression


def train_lr():
    para = {'size': 1500}
    data_source = requests.post('http://localhost:7000/es_virus_data', data=json.dumps(para)).json()
    c_time = []
    modifyTime = []
    confirmed = []
    suspect = []
    cure = []
    dead = []
    for data_list in data_source['hits']['hits']:
        base_info = data_list['_source']
        base_info_2 = base_info['body']
        modifyTime.append([int((base_info_2['modifyTime'] / 1000))])
        try:
            try:
                confirmed.append(base_info_2['confirmedCount'])
                suspect.append(base_info_2['suspectedCount'])
                cure.append(base_info_2['curedCount'])
                dead.append(base_info_2['deadCount'])
            except:
                base_info_1 = str(base_info_2['countRemark'])
                if ('其中' not in base_info_1):
                    confirmed.append(int(re.findall('确诊(.*?)例', base_info_1)[0]))
                    suspect.append(int(re.findall('疑似(.*?)例', base_info_1)[0]))
                    cure.append(int(re.findall('治愈(.*?)例', base_info_1)[0]))
                    dead.append(int(re.findall('死亡(.*?)例', base_info_1)[0]))
                else:
                    confirmed.append(int(re.findall('确诊 (.*?)例', base_info_1)[0]))
                    suspect.append(int(re.findall('疑似 (.*?) 例', base_info_1)[0]))
                    cure.append(int(re.findall('治愈 (.*?) 例', base_info_1)[0]))
                    dead.append(int(re.findall('死亡 (.*?) 例', base_info_1)[0]))
        except:
            dead.append(41)
    data_source = dict({'modifyTime': modifyTime, 'confirmed': confirmed, 'dead': dead, 'suspect': suspect, 'cure': cure})
    print(len(data_source['modifyTime']))
    print(len(data_source['confirmed']))
    print(len(data_source['dead']))
    print(len(data_source['suspect']))
    print(len(data_source['cure']))
    predict_time_line_int = []
    predict_time_line = []
    now = int(time.time())
    for time_skip in range(0, 500000, 200):
        predict_time_line_int.append([(now + time_skip)])
        predict_time_line.append(change_int((now + time_skip)))
    data_predict = {}
    (name, redis_key) = ('ncov_lr_predict', 'predict_result')
    for key_ in ['confirmed', 'suspect', 'dead', 'cure']:
        lr_model = LinearRegression()
        lr_model.fit(data_source['modifyTime'], data_source[key_])
        print('{} predict...'.format(key_))
        dict_name = '{}_list'.format(key_)
        data_predict[dict_name] = [int(result) for result in lr_model.predict(predict_time_line_int)]
    data_predict['predict_timeline'] = predict_time_line
    status = predict_insert_(name, redis_key, data_predict)
    print(status)
