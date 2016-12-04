'''Tests about gzippy.'''

import contextlib
import os
import shutil
import tempfile

@contextlib.contextmanager
def scratch_dir(*args, **kwargs):
    '''With a scratch dir.'''
    try:
        path = tempfile.mkdtemp(*args, **kwargs)
        yield path
    finally:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)

@contextlib.contextmanager
def scratch_file(name, *args, **kwargs):
    '''With a scratch file.'''
    with scratch_dir(*args, **kwargs) as directory:
        yield os.path.join(directory, name)
