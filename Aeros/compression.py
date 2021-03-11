from typing import List
from quart_compress import Compress
from quart import Quart
import warnings


class Base:
    algorithm = 'gzip'

    def __init__(self, level: int = 2, min_size: int = 500, mimetypes: List = None):
        self.compressor = Compress()
        self.level = level
        self.min_size = min_size
        self.mimetypes = mimetypes if mimetypes else ['text/plain', 'text/html', 'text/css', 'text/scss', 'text/xml', 'application/json', 'application/javascript']

    def init_app(self, app: Quart):
        app.config["COMPRESS_ALGORITHM"] = self.algorithm
        app.config["COMPRESS_MIN_SIZE"] = self.min_size
        app.config["COMPRESS_LEVEL"] = self.level
        app.config["COMPRESS_MIMETYPES"] = self.mimetypes
        print("Algorithm is", self.algorithm)
        self.compressor.init_app(app)


class Gzip(Base):
    algorithm = 'gzip'


class Compression:
    def __new__(cls, *args, **kwargs):
        warnings.warn('"Compression" is deprecated. Please use "Gzip" or "Br"!')
        return Gzip(*args, **kwargs)


class Br(Base):
    algorithm = 'br'
