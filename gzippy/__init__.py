"""Wrapper for Gzip file object that keeps track of the internal file obj."""

import builtins
import contextlib

from gzippy.reader import GzipReader
from gzippy.writer import GzipWriter


def from_file(fobj):
    """Open a Gzip file from a file object."""
    if "+" in fobj.mode:
        raise ValueError("Simultaneous reads and writes not supported.")

    if "r" in fobj.mode:
        return GzipReader(fobj)

    if "w" in fobj.mode:
        return GzipWriter(fobj)

    raise ValueError("Mode not supported")


# pylint: disable=redefined-builtin
@contextlib.contextmanager
def open(path, mode="rb"):
    """Open a Gzip file."""
    with builtins.open(path, mode) as raw:
        fobj = from_file(raw)
        try:
            yield fobj
        finally:
            fobj.close()
