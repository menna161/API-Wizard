from flask import Flask, request, jsonify
from gevent import monkey
from gevent.pywsgi import WSGIServer
from bert_model import ManagedBertModel, TextInfillingModel as Model
from service_streamer import Streamer

if (__name__ == '__main__'):
    streamer = Streamer(ManagedBertModel, batch_size=64, max_latency=0.1, worker_num=4, cuda_devices=(0, 1, 2, 3))
    model = Model()
    WSGIServer(('0.0.0.0', 5005), app).serve_forever()
