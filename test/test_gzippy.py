'''Tests about the gzippy top-level functions.'''

import unittest

import gzippy

from . import scratch_file


class GzippyTest(unittest.TestCase):
    '''Tests about the gzippy top-level functions.'''

    def test_open_with_plus(self):
        '''Opening with r+ is not allowed.'''
        with scratch_file('example.gz') as path:
            with open(path, 'w+') as fout:
                pass

            with self.assertRaises(ValueError):
                with gzippy.open(path, 'r+') as fin:
                    pass

    def test_open_with_append(self):
        '''Opening in append mode is not allowed.'''
        with scratch_file('example.gz') as path:
            with open(path, 'w+') as fout:
                pass            

            with self.assertRaises(ValueError):
                with gzippy.open(path, 'ab') as fout:
                    pass
