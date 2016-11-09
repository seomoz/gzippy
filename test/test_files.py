'''Tests about gzippy.files.'''

import os
import subprocess
import unittest

import mock

import gzippy
import gzippy.header

from . import scratch_file, scratch_dir

class FilesTest(unittest.TestCase):
    '''Tests about gzippy'''

    def test_round_trip(self):
        '''Can round-trip content.'''
        content = 'This is some test content.'
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(content)

            with gzippy.open(path, 'rb') as fin:
                self.assertEqual(fin.read(), content)

    def test_unsupported_incremental_reads(self):
        '''Incremental reads are as-of-yet unsupported.'''
        content = 'This is some test content.'
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(content)

            with self.assertRaises(IOError):
                with gzippy.open(path, 'rb') as fin:
                    fin.read(10)

    def test_gzip_compatible(self):
        '''Output compatible with the gzip command-line utility.'''
        content = 'This is some test content.'
        kwargs = {
            'flags': 0,
            'mtime': 1234,
            'name': 'name',
            'comment': 'comment'
        }
        with scratch_dir() as path:
            zipped = os.path.join(path, 'example.gz')
            unzipped = os.path.join(path, 'example')
            with gzippy.GzipWriter.open(zipped, **kwargs) as fout:
                fout.write(content)

            subprocess.check_call(['gunzip', zipped], stderr=subprocess.STDOUT)

            with open(unzipped) as fin:
                self.assertEqual(fin.read(), content)

    def test_lines(self):
        '''Can read the file line by line.'''
        parts = ['some\n', 'lines\n', 'in\n', 'a\n', 'file']
        content = ''.join(parts)
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(content)

            with gzippy.open(path) as fin:
                self.assertEqual(list(fin), parts)

    def test_lines_consolidation(self):
        '''Consolidates lines across multiple chunks.'''
        parts = ['some\n', 'lines\n', 'in\n', 'a\n', 'file']
        chunks = ['so', 'm', 'e\nlines\n', 'i', 'n', '\n', 'a\nfile']
        content = ''.join(chunks)
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(content)

            with gzippy.open(path) as fin:
                with mock.patch.object(fin, 'chunks', iter(chunks)):
                    self.assertEqual(list(fin), parts)

    def test_reader_crc_mismatch(self):
        '''Raises an exception when the crc doesn't match.'''
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write('This is some test content.')

            # Rewrite the last eight bytes
            with open(path, 'r+b') as fout:
                fout.seek(-8, 2)
                fout.write('\xFF' * 8)

            with self.assertRaises(IOError):
                with gzippy.open(path) as fin:
                    fin.read()

    def test_reader_size_mismatch(self):
        '''Raises an exception when the size doesn't match.'''
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write('This is some test content.')

            # Rewrite the last four bytes
            with open(path, 'r+b') as fout:
                fout.seek(-4, 2)
                fout.write('\xFF' * 4)

            with self.assertRaises(IOError):
                with gzippy.open(path) as fin:
                    fin.read()
