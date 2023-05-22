import types
import typing as T
import datetime
import functools
import os
import threading
import traceback
from .. import common
from . import expression, util
import uuid
from .app import SchedyApp
from .schedule import Schedule
from .actor.base import ActorBase


def set_value_manually(self, expr_raw: str=None, value: T.Any=None, force_resend: bool=False, rescheduling_delay: T.Union[(float, int, datetime.datetime, datetime.timedelta)]=None) -> None:
    'Evaluates the given expression or value and sets the result.\n        An existing re-scheduling timer is cancelled and a new one is\n        started if re-scheduling timers are configured.\n        rescheduling_delay, if given, overwrites the value configured\n        for the room. Passing 0 disables re-scheduling.'
    _checks = ((expr_raw is None), (value is None))
    if (all(_checks) or (not any(_checks))):
        raise ValueError('specify exactly one of expr_raw and value')
    markers = set()
    now = self.app.datetime()
    if (expr_raw is not None):
        try:
            expr = util.compile_expression(expr_raw)
        except SyntaxError:
            for line in traceback.format_exc(limit=0):
                self.log(line.rstrip(os.linesep), level='ERROR')
            self.log('Failed expression: {}'.format(repr(expr_raw)), level='ERROR')
            return
        env = expression.build_expr_env(self, now)
        result = self.eval_expr(expr, env)
        self.log('Evaluated expression {} to {}.'.format(repr(expr_raw), repr(result)), level='DEBUG')
        if isinstance(result, Exception):
            self.log('Failed expression: {}'.format(repr(expr_raw)), level='ERROR')
            return
        if isinstance(result, expression.types.Mark):
            result = result.unwrap(markers)
        not_allowed_result_types = (expression.types.ControlResult, expression.types.Postprocessor, type(None))
        value = None
        if isinstance(result, expression.types.IncludeSchedule):
            _result = result.schedule.evaluate(self, now)
            if (_result is not None):
                value = _result[0]
                markers.update(_result[1])
        elif (not isinstance(result, not_allowed_result_types)):
            value = result
    if (value is not None):
        value = self.validate_value(value)
    if (value is None):
        self.log('Ignoring value.')
        return
    if (expression.types.Mark.OVERLAY in markers):
        self._store_for_overlaying()
    self.set_value(value, force_resend=force_resend)
    if (rescheduling_delay != 0):
        self.start_rescheduling_timer(delay=rescheduling_delay)
    else:
        self.cancel_rescheduling_timer()
