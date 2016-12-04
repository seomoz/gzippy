'''Tests about gzippy.'''

import unittest

from six.moves import cStringIO as StringIO

from gzippy.header import Header


class HeaderTest(unittest.TestCase):
    '''Tests about the gzippy header.'''

    def setUp(self):
        self.header = Header(
            flags=(Header.FEXTRA | Header.FNAME | Header.FCOMMENT),
            mtime=1234, 
            extra_flags=3,
            os_flags=1,
            extra='extra',
            name='name',
            comment='comment')

    def test_round_trip(self):
        '''Can round-trip headers.'''
        fout = StringIO()
        self.header.write(fout)
        self.assertEqual(Header.read(StringIO(fout.getvalue())), self.header)

    def test_invalid_magic(self):
        '''Raises an exception if the magic is wrong.'''
        with self.assertRaises(IOError):
            Header.read(StringIO('Not the right magic'))

    def test_invalid_method(self):
        '''Only the deflate method is supported.'''
        with self.assertRaises(IOError):
            Header.read(StringIO('\x1F\x8B\xFF'))

    def test_multipart_not_supported(self):
        '''Raises an exception if the header has the multibyte flag.'''
        # This is a very basic header, with just FMULTI set
        serialized = StringIO('\x1F\x8B\x08\x02\xD2\x04\x00\x00\x03\x01')
        with self.assertRaises(ValueError):
            Header.read(serialized)

    def test_repr(self):
        '''Exercises the repr function.'''
        parts = [
            '<Gzip.Header',
            'flags=28,',
            'mtime=1234,',
            'extra_flags=3,',
            'os_flags=1,',
            'extra=extra,',
            'name=name,',
            'comment=comment>'
        ]
        self.assertEqual(repr(self.header), ' '.join(parts))
