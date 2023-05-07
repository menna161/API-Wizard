import os
import sys
import types
import inspect
import datetime
import pkg_resources
import pytest
import tornado
import tornado.gen
import tornado.testing
import tornado.httpserver
import tornado.httpclient


@pytest.mark.tryfirst
def pytest_pyfunc_call(pyfuncitem):
    gen_test_mark = pyfuncitem.get_closest_marker('gen_test')
    if gen_test_mark:
        io_loop = pyfuncitem.funcargs.get('io_loop')
        run_sync = gen_test_mark.kwargs.get('run_sync', True)
        funcargs = dict(((arg, pyfuncitem.funcargs[arg]) for arg in _argnames(pyfuncitem.obj)))
        if iscoroutinefunction(pyfuncitem.obj):
            coroutine = pyfuncitem.obj
            future = tornado.gen.convert_yielded(coroutine(**funcargs))
        else:
            coroutine = tornado.gen.coroutine(pyfuncitem.obj)
            future = coroutine(**funcargs)
        if run_sync:
            io_loop.run_sync((lambda : future), timeout=_timeout(pyfuncitem))
        else:
            future_with_timeout = tornado.gen.with_timeout(datetime.timedelta(seconds=_timeout(pyfuncitem)), future)
            io_loop.add_future(future_with_timeout, (lambda f: io_loop.stop()))
            io_loop.start()
            future_with_timeout.result()
        return True
