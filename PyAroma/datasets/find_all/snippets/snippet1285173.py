from __future__ import unicode_literals
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.cache import SimpleCache
from prompt_toolkit.clipboard import Clipboard, InMemoryClipboard
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.eventloop import get_event_loop, ensure_future, Return, run_in_executor, run_until_complete, call_from_executor, From
from prompt_toolkit.eventloop.base import get_traceback_from_context
from prompt_toolkit.filters import to_filter, Condition
from prompt_toolkit.input.base import Input
from prompt_toolkit.input.defaults import get_default_input
from prompt_toolkit.input.typeahead import store_typeahead, get_typeahead
from prompt_toolkit.key_binding.bindings.page_navigation import load_page_navigation_bindings
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, ConditionalKeyBindings, KeyBindingsBase, merge_key_bindings, GlobalOnlyKeyBindings
from prompt_toolkit.key_binding.key_processor import KeyProcessor
from prompt_toolkit.key_binding.emacs_state import EmacsState
from prompt_toolkit.key_binding.vi_state import ViState
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.dummy import create_dummy_layout
from prompt_toolkit.layout.layout import Layout, walk
from prompt_toolkit.output import Output, ColorDepth
from prompt_toolkit.output.defaults import get_default_output
from prompt_toolkit.renderer import Renderer, print_formatted_text
from prompt_toolkit.search import SearchState
from prompt_toolkit.styles import BaseStyle, default_ui_style, default_pygments_style, merge_styles, DynamicStyle, DummyStyle, StyleTransformation, DummyStyleTransformation
from prompt_toolkit.utils import Event, in_main_thread
from .current import set_app
from .run_in_terminal import run_in_terminal, run_coroutine_in_terminal
from subprocess import Popen
from traceback import format_tb
import os
import re
import signal
import six
import sys
import time
from prompt_toolkit.shortcuts import PromptSession


@property
def _key_bindings(self):
    current_window = self.app.layout.current_window
    other_controls = list(self.app.layout.find_all_controls())
    key = (current_window, frozenset(other_controls))
    return self._cache.get(key, (lambda : self._create_key_bindings(current_window, other_controls)))
