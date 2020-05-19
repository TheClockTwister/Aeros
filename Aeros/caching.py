from .patches.flask_caching import Cache


class SimpleCache(Cache):
    def __init__(self, *args, **kwargs):
        Cache.__init__(self, *args, **kwargs)
        self.config["CACHE_TYPE"] = "simple"


class FilesystemCache(Cache):
    def __init__(self, directory: str, *args, **kwargs):
        Cache.__init__(self, *args, **kwargs)
        self.config["CACHE_TYPE"] = "filesystem"
        self.config["CACHE_DIR"] = directory


class RedisCache(Cache):
    def __init__(self, host: str, port: int, password: str = "", db: int = 0, *args, **kwargs):
        Cache.__init__(self, *args, **kwargs)
        self.config["CACHE_TYPE"] = "redis"
        self.config["CACHE_REDIS_HOST"] = host
        self.config["CACHE_REDIS_PORT"] = port
        self.config["CACHE_REDIS_PASSWORD"] = password
        self.config["CACHE_REDIS_DB"] = db
