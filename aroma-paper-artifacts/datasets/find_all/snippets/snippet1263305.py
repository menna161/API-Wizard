from itertools import chain
from copy import deepcopy
from keyword import iskeyword as is_python_keyword
from functools import update_wrapper
from jinja2 import nodes
from jinja2.nodes import EvalContext
from jinja2.visitor import NodeVisitor
from jinja2.optimizer import Optimizer
from jinja2.exceptions import TemplateAssertionError
from jinja2.utils import Markup, concat, escape
from jinja2._compat import range_type, text_type, string_types, iteritems, NativeStringIO, imap, izip
from jinja2.idtracking import Symbols, VAR_LOAD_PARAMETER, VAR_LOAD_RESOLVE, VAR_LOAD_ALIAS, VAR_LOAD_UNDEFINED
from jinja2.runtime import __all__ as exported


def visit_For(self, node, frame):
    loop_frame = frame.inner()
    test_frame = frame.inner()
    else_frame = frame.inner()
    extended_loop = (node.recursive or ('loop' in find_undeclared(node.iter_child_nodes(only=('body',)), ('loop',))))
    loop_ref = None
    if extended_loop:
        loop_ref = loop_frame.symbols.declare_parameter('loop')
    loop_frame.symbols.analyze_node(node, for_branch='body')
    if node.else_:
        else_frame.symbols.analyze_node(node, for_branch='else')
    if node.test:
        loop_filter_func = self.temporary_identifier()
        test_frame.symbols.analyze_node(node, for_branch='test')
        self.writeline(('%s(fiter):' % self.func(loop_filter_func)), node.test)
        self.indent()
        self.enter_frame(test_frame)
        self.writeline(((self.environment.is_async and 'async for ') or 'for '))
        self.visit(node.target, loop_frame)
        self.write(' in ')
        self.write(((self.environment.is_async and 'auto_aiter(fiter)') or 'fiter'))
        self.write(':')
        self.indent()
        self.writeline('if ', node.test)
        self.visit(node.test, test_frame)
        self.write(':')
        self.indent()
        self.writeline('yield ')
        self.visit(node.target, loop_frame)
        self.outdent(3)
        self.leave_frame(test_frame, with_python_scope=True)
    if node.recursive:
        self.writeline(('%s(reciter, loop_render_func, depth=0):' % self.func('loop')), node)
        self.indent()
        self.buffer(loop_frame)
        else_frame.buffer = loop_frame.buffer
    if extended_loop:
        self.writeline(('%s = missing' % loop_ref))
    for name in node.find_all(nodes.Name):
        if ((name.ctx == 'store') and (name.name == 'loop')):
            self.fail("Can't assign to special loop variable in for-loop target", name.lineno)
    if node.else_:
        iteration_indicator = self.temporary_identifier()
        self.writeline(('%s = 1' % iteration_indicator))
    self.writeline(((self.environment.is_async and 'async for ') or 'for '), node)
    self.visit(node.target, loop_frame)
    if extended_loop:
        if self.environment.is_async:
            self.write((', %s in await make_async_loop_context(' % loop_ref))
        else:
            self.write((', %s in LoopContext(' % loop_ref))
    else:
        self.write(' in ')
    if node.test:
        self.write(('%s(' % loop_filter_func))
    if node.recursive:
        self.write('reciter')
    else:
        if (self.environment.is_async and (not extended_loop)):
            self.write('auto_aiter(')
        self.visit(node.iter, frame)
        if (self.environment.is_async and (not extended_loop)):
            self.write(')')
    if node.test:
        self.write(')')
    if node.recursive:
        self.write(', undefined, loop_render_func, depth):')
    else:
        self.write(((extended_loop and ', undefined):') or ':'))
    self.indent()
    self.enter_frame(loop_frame)
    self.blockvisit(node.body, loop_frame)
    if node.else_:
        self.writeline(('%s = 0' % iteration_indicator))
    self.outdent()
    self.leave_frame(loop_frame, with_python_scope=(node.recursive and (not node.else_)))
    if node.else_:
        self.writeline(('if %s:' % iteration_indicator))
        self.indent()
        self.enter_frame(else_frame)
        self.blockvisit(node.else_, else_frame)
        self.leave_frame(else_frame)
        self.outdent()
    if node.recursive:
        self.return_buffer_contents(loop_frame)
        self.outdent()
        self.start_write(frame, node)
        if self.environment.is_async:
            self.write('await ')
        self.write('loop(')
        if self.environment.is_async:
            self.write('auto_aiter(')
        self.visit(node.iter, frame)
        if self.environment.is_async:
            self.write(')')
        self.write(', loop)')
        self.end_write(frame)
