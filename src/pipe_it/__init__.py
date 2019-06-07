import functools
import itertools
import socket
import sys
from contextlib import closing
from collections import deque
import yaml

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

import log_it
log = log_it.logger(__name__)


class pipe:
    def __init__(self, pipe_func):
        self.pipe_func = pipe_func
        functools.update_wrapper(self, pipe_func)

    def __ror__(self, other):
        return self.pipe_func(other)

    def __call__(self, *args, **kwargs):
        return pipe(lambda x: self.pipe_func(x, *args, **kwargs))


@pipe
def first(items):
    for item in items:
        return item

@pipe
def select(item, func=None):
    return func(item)

# @pipe
# def join(items, spacer="\n"):
#     return spacer.joint(items)

@pipe
def apply(items, func=None):
    for item in items:
        yield func(item)


@pipe
def where(items, predicate=None):
    for item in items:
        if predicate(item):
            yield item


@pipe
def from_yaml(items):
    for item in items:
        yield yaml.safe_load(item)


@pipe
def tee_log(items):
    for item in items:
        log.info(item)
        yield item

@pipe
def drain(items):
    for _ in items:
        pass