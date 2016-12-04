'''A reader of gzip files.'''

import struct
import zlib

from .header import Header


class GzipReader(object):
    '''A reader of gzip files.'''

    def __init__(self, fobj):
        self.raw = fobj
        self.crc = zlib.crc32('') & 0xFFFFFFFF
        self.size = 0
        self.decompressobj = zlib.decompressobj(-zlib.MAX_WBITS)
        self.header = Header.read(self.raw)
        self.chunks = iter(self.chunks_generator())

    def chunks_generator(self):
        '''Generator of decompressed data.'''
        buf = self.raw.read(4096)
        while buf:
            uncompressed = self.decompressobj.decompress(buf)
            self.size += len(uncompressed)
            self.crc = zlib.crc32(uncompressed, self.crc) & 0xFFFFFFFF
            yield uncompressed
            buf = self.raw.read(4096)

        # Yield the last flushed block
        uncompressed = self.decompressobj.flush()
        self.size += len(uncompressed)
        self.crc = zlib.crc32(uncompressed, self.crc) & 0xFFFFFFFF
        yield uncompressed

        # Check the CRC and size
        crc, size = struct.unpack('<II', self.decompressobj.unused_data[-8:])
        if crc != self.crc:
            raise IOError('CRC mismatch: %s (read) != %s (computed)' % (crc, self.crc))
        if size != self.size:
            raise IOError('Size mismatch: %s (read) != %s (computed)' % (size, self.size))

    def lines(self):
        '''Generator of the lines in a file.'''
        last = ''
        for chunk in self.chunks:
            chunk = last + chunk
            start = 0
            index = chunk.find('\n')
            while index != -1:
                yield chunk[start:index+1]
                start, index = index + 1, chunk.find('\n', index + 1)

            last = chunk[start:]

        yield last

    def __iter__(self):
        '''Generator of the lines in this file.'''
        return self.lines()

    def read(self, size=-1):
        '''Read data from the file.'''
        if size == -1:
            return ''.join(self.chunks)
        else:
            raise IOError('Incremental reads not supported.')

    def close(self):
        '''Close the file.'''
        self.raw.close()
