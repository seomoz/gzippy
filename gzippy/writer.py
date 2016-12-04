'''A writer of gzip files.'''

import contextlib
import struct
import zlib

from .header import Header


class GzipWriter(object):
    '''A writer of gzip files.'''

    @classmethod
    @contextlib.contextmanager
    def open(cls, path, *args, **kwargs):
        '''Open the provided path.'''
        with contextlib.closing(cls(open(path, 'wb'), *args, **kwargs)) as fout:
            yield fout

    def __init__(self, fobj, compresslevel=9, **kwargs):
        self.raw = fobj
        self.crc = zlib.crc32('') & 0xFFFFFFFF
        self.size = 0
        self.compressobj = zlib.compressobj(compresslevel,
                                            zlib.DEFLATED,
                                            -zlib.MAX_WBITS,
                                            zlib.DEF_MEM_LEVEL,
                                            0)

        # Write the header
        self.header = Header(**kwargs)
        self.header.write(self.raw)

    def close(self):
        '''Close the file.'''
        try:
            self.raw.write(self.compressobj.flush(zlib.Z_FINISH))
            self.raw.write(struct.pack('<II', self.crc, self.size))
            self.raw.flush()
        finally:
            self.raw.close()

    def write(self, data):
        '''Write data to the file.'''
        self.raw.write(self.compressobj.compress(data))
        self.size += len(data)
        self.crc = zlib.crc32(data, self.crc) & 0xFFFFFFFF
