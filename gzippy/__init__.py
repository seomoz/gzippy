'''Gzip file interactions.'''

import contextlib

from six.moves import builtins

from .reader import GzipReader
from .writer import GzipWriter


def from_file(fobj):
    '''Open a Gzip file from a file object.'''
    if '+' in fobj.mode:
        raise ValueError('Simultaneous reads and writes not supported.')
    elif 'r' in fobj.mode:
        return GzipReader(fobj)
    elif 'w' in fobj.mode:
        return GzipWriter(fobj)
    else:
        raise ValueError('Mode not supported')


# pylint: disable=redefined-builtin
@contextlib.contextmanager
def open(path, mode='rb'):
    '''Open a Gzip file.'''
    with builtins.open(path, mode) as raw:
        fobj = from_file(raw)
        try:
            yield fobj
        finally:
            fobj.close()
