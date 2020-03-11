'''Tests about gzippy.files.'''

import os
import subprocess
import unittest

import mock

import gzippy

from . import scratch_file, scratch_dir

class FilesTest(unittest.TestCase):
    '''Tests about gzippy'''

    def test_round_trip(self):
        '''Can round-trip content.'''
        content = b'This is some test content.'
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(content)

            with gzippy.open(path, 'rb') as fin:
                self.assertEqual(fin.read(), content)

    def test_incremental_reads(self):
        '''Incremental reads'''
        content = b'This is some test content.'
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(content)

            with gzippy.open(path, 'rb') as fin:
                self.assertEqual(fin.read(10), content[:10])

    def test_gzip_compatible(self):
        '''Output compatible with the gzip command-line utility.'''
        content = b'This is some test content.'

        with scratch_dir() as path:
            zipped = os.path.join(path, 'example.gz')
            unzipped = os.path.join(path, 'example')
            with gzippy.GzipWriter.open(zipped) as fout:
                fout.write(content)

            subprocess.check_call(['gunzip', zipped], stderr=subprocess.STDOUT)

            with open(unzipped, 'rb') as fin:
                self.assertEqual(fin.read(), content)

    def test_lines(self):
        '''Can read the file line by line.'''
        parts = [b'some\n', b'lines\n', b'in\n', b'a\n', b'file']
        content = b''.join(parts)
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(content)

            with gzippy.open(path) as fin:
                self.assertEqual(list(fin), parts)

    def test_lines_consolidation(self):
        '''Consolidates lines across multiple chunks.'''
        parts = [b'some\n', b'lines\n', b'in\n', b'a\n', b'file']
        chunks = [b'so', b'm', b'e\nlines\n', b'i', b'n', b'\n', b'a\nfile']
        content = b''.join(chunks)
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(content)

            with gzippy.open(path) as fin:
                self.assertEqual(list(fin), parts)

    def test_reader_crc_mismatch(self):
        '''Raises an exception when the crc doesn't match.'''
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(b'This is some test content.')

            # Rewrite the last eight bytes
            with open(path, 'r+b') as fout:
                fout.seek(-8, 2)
                fout.write(b'\xFF' * 8)

            with self.assertRaises(IOError):
                with gzippy.open(path) as fin:
                    fin.read()

    def test_reader_size_mismatch(self):
        '''Raises an exception when the size doesn't match.'''
        with scratch_file('example.gz') as path:
            with gzippy.open(path, 'wb') as fout:
                fout.write(b'This is some test content.')

            # Rewrite the last four bytes
            with open(path, 'r+b') as fout:
                fout.seek(-4, 2)
                fout.write(b'\xFF' * 4)

            with self.assertRaises(IOError):
                with gzippy.open(path) as fin:
                    fin.read()
