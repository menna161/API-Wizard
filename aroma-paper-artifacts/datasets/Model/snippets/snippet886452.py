from bert_model import TextInfillingModel as Model
from flask import Flask, request, jsonify
from service_streamer import ThreadedStreamer

if (__name__ == '__main__'):
    model = Model()
    streamer = ThreadedStreamer(model.predict, batch_size=64, max_latency=0.1)
    app.run(port=5005, debug=False)
