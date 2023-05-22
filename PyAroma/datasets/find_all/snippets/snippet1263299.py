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


def visit_Template(self, node, frame=None):
    assert (frame is None), 'no root frame allowed'
    eval_ctx = EvalContext(self.environment, self.name)
    from jinja2.runtime import __all__ as exported
    self.writeline(('from __future__ import %s' % ', '.join(code_features)))
    self.writeline(('from jinja2.runtime import ' + ', '.join(exported)))
    if self.environment.is_async:
        self.writeline('from jinja2.asyncsupport import auto_await, auto_aiter, make_async_loop_context')
    envenv = (((not self.defer_init) and ', environment=environment') or '')
    have_extends = (node.find(nodes.Extends) is not None)
    for block in node.find_all(nodes.Block):
        if (block.name in self.blocks):
            self.fail(('block %r defined twice' % block.name), block.lineno)
        self.blocks[block.name] = block
    for import_ in node.find_all(nodes.ImportedName):
        if (import_.importname not in self.import_aliases):
            imp = import_.importname
            self.import_aliases[imp] = alias = self.temporary_identifier()
            if ('.' in imp):
                (module, obj) = imp.rsplit('.', 1)
                self.writeline(('from %s import %s as %s' % (module, obj, alias)))
            else:
                self.writeline(('import %s as %s' % (imp, alias)))
    self.writeline(('name = %r' % self.name))
    self.writeline(('%s(context, missing=missing%s):' % (self.func('root'), envenv)), extra=1)
    self.indent()
    self.write_commons()
    frame = Frame(eval_ctx)
    if ('self' in find_undeclared(node.body, ('self',))):
        ref = frame.symbols.declare_parameter('self')
        self.writeline(('%s = TemplateReference(context)' % ref))
    frame.symbols.analyze_node(node)
    frame.toplevel = frame.rootlevel = True
    frame.require_output_check = (have_extends and (not self.has_known_extends))
    if have_extends:
        self.writeline('parent_template = None')
    self.enter_frame(frame)
    self.pull_dependencies(node.body)
    self.blockvisit(node.body, frame)
    self.leave_frame(frame, with_python_scope=True)
    self.outdent()
    if have_extends:
        if (not self.has_known_extends):
            self.indent()
            self.writeline('if parent_template is not None:')
        self.indent()
        if (supports_yield_from and (not self.environment.is_async)):
            self.writeline('yield from parent_template.root_render_func(context)')
        else:
            self.writeline(('%sfor event in parent_template.root_render_func(context):' % ((self.environment.is_async and 'async ') or '')))
            self.indent()
            self.writeline('yield event')
            self.outdent()
        self.outdent((1 + (not self.has_known_extends)))
    for (name, block) in iteritems(self.blocks):
        self.writeline(('%s(context, missing=missing%s):' % (self.func(('block_' + name)), envenv)), block, 1)
        self.indent()
        self.write_commons()
        block_frame = Frame(eval_ctx)
        undeclared = find_undeclared(block.body, ('self', 'super'))
        if ('self' in undeclared):
            ref = block_frame.symbols.declare_parameter('self')
            self.writeline(('%s = TemplateReference(context)' % ref))
        if ('super' in undeclared):
            ref = block_frame.symbols.declare_parameter('super')
            self.writeline(('%s = context.super(%r, block_%s)' % (ref, name, name)))
        block_frame.symbols.analyze_node(block)
        block_frame.block = name
        self.enter_frame(block_frame)
        self.pull_dependencies(block.body)
        self.blockvisit(block.body, block_frame)
        self.leave_frame(block_frame, with_python_scope=True)
        self.outdent()
    self.writeline(('blocks = {%s}' % ', '.join((('%r: block_%s' % (x, x)) for x in self.blocks))), extra=1)
    self.writeline(('debug_info = %r' % '&'.join((('%s=%s' % x) for x in self.debug_info))))
