"""
The compression module includes classes for compression algorithms implemented by `quart_compress`.
These are compatible with the async coroutine framework that Aeros uses and will compress the web
server's responses before sending it to the client.
"""

from typing import List
from quart_compress import Compress
from quart import Quart
import warnings


class Base:
    """
    The base class that implements the wrapper for `quart_compress.Compress`.
    """
    algorithm = 'gzip'

    def __init__(self, level: int = 2, min_size: int = 500, mimetypes: List = None):
        self.compressor = Compress()
        self.level = level
        self.min_size = min_size
        self.mimetypes = mimetypes if mimetypes else ['text/plain', 'text/html', 'text/css', 'text/scss', 'text/xml', 'application/json', 'application/javascript']

    def init_app(self, app: Quart):
        """
        Initializes the `Compress` instance with the give `WebServer`/`Quart` application instance

        Arguments:
            app (Quart): The web server instance to use the caching functionality with
        """
        app.config["COMPRESS_ALGORITHM"] = self.algorithm
        app.config["COMPRESS_MIN_SIZE"] = self.min_size
        app.config["COMPRESS_LEVEL"] = self.level
        app.config["COMPRESS_MIMETYPES"] = self.mimetypes
        print("Algorithm is", self.algorithm)
        self.compressor.init_app(app)


class Gzip(Base):
    """
    This class should be used to implement a Gzip compression to your Aeros web server.
    """
    algorithm = 'gzip'


class Br(Base):
    """
    This class should be used to implement a Br compression to your Aeros web server.
    """
    algorithm = 'br'


class Compression:
    """
    The former class that represented compression for Aeros. Falls back to `Gzip`.

    .. warning::
        This class is deprecated and should not be used. Use `Gzip` or `Br` instead.
    """

    def __new__(cls, *args, **kwargs):
        warnings.warn('"Compression" is deprecated. Please use "Gzip" or "Br" instead.')
        return Gzip(*args, **kwargs)
