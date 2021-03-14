"""
This module contains features for server-side caching by wrapping the `flask_caching` module.
"""

from flask_caching import Cache
import warnings


class SimpleCache(Cache):
    """ The most basic cache that requires no set-up and no arguments. """

    def __new__(cls, *args, **kwargs):
        return Cache(
            *args, **kwargs,
            config={
                'CACHE_TYPE': cls.__name__
            })


class FileSystemCache(Cache):
    """ Stores cached responses on the file system,
    good for huge caches that don't fit into memory."""

    def __new__(cls, directory: str, *args, **kwargs):
        return Cache(
            *args, **kwargs,
            config={
                'CACHE_TYPE': cls.__name__,
                'CACHE_DIR': directory
            })


# For backwards compatibility
class FilesystemCache:
    """ An alias for `FileSystemCache`

    .. warning::
        This class is deprecated! Use `FileSystemCache` instead.
    """

    def __new__(cls, *args, **kwargs):
        warnings.warn('"FilesystemCache" is deprecated! Use "FileSystemCache" instead.')
        return FileSystemCache(
            *args, **kwargs
        )


class RedisCache(Cache):
    """ A Redis client to store responses on an external Redis server. """

    # ignore different signature
    def __new__(cls, host: str, port: int, user: str, password: str, db: str, *args, **kwargs):
        return Cache(
            *args, **kwargs,
            config={
                'CACHE_TYPE': cls.__name__,
                'CACHE_REDIS_HOST': host,
                'CACHE_REDIS_PORT': port,
                'CACHE_REDIS_PASSWORD': password,
                'CACHE_REDIS_DB': db
            })
