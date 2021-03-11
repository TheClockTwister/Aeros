from flask_caching import Cache
import warnings


class SimpleCache(Cache):
    def __new__(cls, *args, **kwargs):
        return Cache(
            *args, **kwargs,
            config={
                'CACHE_TYPE': cls.__name__
            })


class FileSystemCache(Cache):
    def __new__(cls, directory: str, *args, **kwargs):
        return Cache(
            *args, **kwargs,
            config={
                'CACHE_TYPE': cls.__name__,
                'CACHE_DIR': directory
            })


# For backwards compatibility
class FilesystemCache:
    def __new__(cls, *args, **kwargs):
        warnings.warn('"FilesystemCache" is deprecated! Use "FileSystemCache" instead.')
        return FileSystemCache(
            *args, **kwargs
        )


class RedisCache(Cache):
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
