'''Classes to help with reading and wrigin headers.'''

import struct
import time
import zlib


# pylint: disable=too-many-instance-attributes
class Header(object):
    '''Read, write, hold Gzip file headers.'''

    # Constatnts
    MAGIC = '\x1F\x8B'
    METHOD = chr(zlib.DEFLATED)

    # Flags
    FTEXT = 0x1
    FMULTI = 0x2
    FEXTRA = 0x4
    FNAME = 0x8
    FCOMMENT = 0x10

    # The attributes for this class
    __slots__ = (
        'flags',
        'mtime',
        'extra_flags',
        'os_flags',
        'extra',
        'name',
        'comment',
    )

    # pylint: disable=too-many-arguments
    def __init__(self, flags=0, mtime=None, extra_flags=2, os_flags=255, extra=None,
                 name=None, comment=None):
        self.flags = flags
        self.mtime = mtime or int(time.time())
        self.extra_flags = extra_flags
        self.os_flags = os_flags
        # TODO(dan): make extra access like a dictionary
        self.extra = extra
        self.name = name
        self.comment = comment

    @classmethod
    def read_null_terminated(cls, fobj):
        '''Read a null-terminated string.'''
        result = ''
        while True:
            char = fobj.read(1)
            if not char or char == '\x00':
                break
            result += char
        return result

    @classmethod
    def read(cls, fobj):
        '''Read in headers from a file object.'''
        if fobj.read(2) != cls.MAGIC:
            raise IOError('Invalid magic.')
        if fobj.read(1) != cls.METHOD:
            raise IOError('Unknown compression method')
        flags = ord(fobj.read(1))
        mtime = struct.unpack('<L', fobj.read(4))[0]
        extra_flags = ord(fobj.read(1))
        os_flags = ord(fobj.read(1))

        extra = None
        if flags & cls.FEXTRA:
            length = struct.unpack('<H', fobj.read(2))[0]
            extra = fobj.read(length)

        name = None
        if flags & cls.FNAME:
            raw = cls.read_null_terminated(fobj)
            name = raw.decode('latin-1')

        comment = None
        if flags & cls.FCOMMENT:
            comment = cls.read_null_terminated(fobj).decode('latin-1')

        if flags & cls.FMULTI:
            raise ValueError('Multipart gzips not supported.')

        return cls(flags, mtime, extra_flags, os_flags, extra, name,
                   comment)

    def write(self, fobj):
        '''Write this header to a file object.'''
        self.flags = (
            (self.FNAME if (self.name is not None) else 0) |
            (self.FEXTRA if (self.extra is not None) else 0) |
            (self.FCOMMENT if (self.comment is not None) else 0))

        fobj.write(self.MAGIC)                      # magic header
        fobj.write(self.METHOD)                     # compression method
        fobj.write(chr(self.flags))                 # flags
        fobj.write(struct.pack('<L', self.mtime))   # Modification time
        fobj.write(chr(self.extra_flags))           # eXtra FLags (max compression)
        fobj.write(chr(self.os_flags))              # Operating system (unknown)

        if (self.flags & self.FEXTRA) and self.extra:
            fobj.write(struct.pack('<H', len(self.extra)))
            fobj.write(self.extra)

        if (self.flags & self.FNAME) and self.name:
            fobj.write(self.name)
            fobj.write('\000')

        if (self.flags & self.FCOMMENT) and self.comment:
            fobj.write(self.comment)
            fobj.write('\000')

    def __repr__(self):
        joined = ', '.join(
            '%s=%s' % (attr, getattr(self, attr)) for attr in self.__slots__)
        return '<Gzip.Header %s>' % joined

    def __eq__(self, other):
        return all(
            getattr(self, attr) == getattr(other, attr) for attr in self.__slots__)
