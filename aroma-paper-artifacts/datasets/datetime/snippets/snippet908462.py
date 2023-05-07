import copy
import datetime
import urllib
import webapp2
import jinja2
import os
from core.callhistory import CallHistory
from core.board import Board
from core.deal import Deal
from core.position import Position
from core.call import Pass
from z3b.bidder import Interpreter, Bidder, InconsistentHistoryException
from proxy import ConstraintsSerializer
import json


def get(self):
    bidder = Bidder()
    board = self._board_from_request()
    until_position_string = self.request.get('until_position')
    until_position = (Position.from_char(until_position_string) if until_position_string else None)
    call_selections = self._bid_all_hands(bidder, board, until_position=until_position)
    until_position_history_string = board.call_history.calls_string()
    call_selections += self._bid_all_hands(bidder, board)
    board_dict = {'board_number': board.number, 'calls_string': until_position_history_string, 'autobid_continuation': board.call_history.calls_string(), 'autobid_interpretations': map(self._json_tuple, call_selections)}
    self.response.headers['Content-Type'] = 'application/json'
    self.response.headers['Cache-Control'] = 'public'
    expires_date = (datetime.datetime.utcnow() + datetime.timedelta(days=1))
    expires_str = expires_date.strftime('%d %b %Y %H:%M:%S GMT')
    self.response.headers.add_header('Expires', expires_str)
    self.response.out.write(json.dumps(board_dict))
