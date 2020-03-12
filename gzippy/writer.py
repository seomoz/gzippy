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
        self.name = fobj.name

        self.gzip = gzip.GzipFile(
            filename=self.name,
            fileobj=self.raw,
            compresslevel=compresslevel,
            **kwargs
        )

    def __getattr__(self, attr):
        """Delegate attributes to internal object."""
        return getattr(self.raw, attr)

    def close(self):
        """Close the file."""
        self.gzip.flush()
        self.gzip.close()
        self.raw.close()

    def write(self, data):
        """Write data to the file."""
        self.gzip.write(data)
