"""A reader of gzip files."""

import gzip


class GzipReader:
    """A reader of gzip files."""

    def __init__(self, fobj):
        """Store input object & handle Gzip object using it."""
        self.raw = fobj
        self.name = fobj.name

        self.gzip = gzip.GzipFile(filename=self.name, fileobj=self.raw)

    def __getattr__(self, attr):
        """Delegate attributes to internal object."""
        return getattr(self.raw, attr)

    def readlines(self):
        """Delegate readlines call to internal gzip object."""
        yield from self.gzip.readlines()

    def __iter__(self):
        """Line by line iterator over the internal contents of the file."""
        yield from self.readlines()

    def read(self, size=-1):
        """Read data from the file."""
        return self.gzip.read(size)

    def close(self):
        """Close the file."""
        self.raw.close()
