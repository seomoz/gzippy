"""Provides ability to open & write Gzip files."""

import gzip

from contextlib import closing, contextmanager


class GzipWriter:
    """A writer of gzip files."""

    @classmethod
    @contextmanager
    def open(cls, path, *args, **kwargs):
        """Open the provided path."""
        with closing(cls(open(path, "wb"), *args, **kwargs)) as fout:
            yield fout

    def __init__(self, fobj, compresslevel=9, **kwargs):
        """Construct instance of class around the input file obj."""
        self.raw = fobj
        self.gzip = gzip.GzipFile(
            fileobj=fobj, compresslevel=compresslevel, **kwargs
        )

    def close(self):
        """Close the file."""
        self.gzip.flush()
        self.gzip.close()
        self.raw.close()

    def write(self, data):
        """Write data to the file."""
        if isinstance(data, str):
            self.gzip.write(bytes(data, "latin-1"))
        else:
            self.gzip.write(data)
