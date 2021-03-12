"""
This module contains the main web server class
"""

import functools
import inspect
from quart import Quart
import hashlib
import uvicorn
import logging
import logging.handlers
from logging import INFO
import sys

from .caching.server import Cache
from .compression import Base
from .Request import EasyRequest


class WebServer(Quart):
    """ This is the main server class which extends a standard Flask class by a bunch of features and major
    performance improvements. It extends the quart class, which by itself is already an enhanced version of
    the Flask class. This class however allows production-grade deployment using the uvicorn ASGI server
    as production server. But instead of calling the uvicorn command via the console, it can be started
    directly from the Python code itself, making it easier to integrate in higher-level scripts and
    applications without calling os.system() or subprocess.Popen().
    """

    __log_format_std = '[%(asctime)s] %(levelname)s: %(message)s'  # for instance logger "quart.app"

    def __init__(self, import_name: str, host: str = "0.0.0.0", port: int = 80, include_server_header: bool = True,
                 logging_level: int = INFO, cache: Cache = None, compression: Base = None,
                 global_headers: dict = {}, *args, **kwargs):

        super().__init__(import_name, *args, **kwargs)

        self.log_level = logging_level
        self.logger.setLevel(self.log_level)
        self._host, self._port = host, port

        self._cache = cache
        self._compression = compression

        h = logging.StreamHandler(sys.stdout)  # make own logging format the same as uvicorn uses
        h.setFormatter(logging.Formatter(self.__log_format_std))
        self.logger.handlers = [h]

        self._global_headers = global_headers
        if include_server_header:
            self._global_headers['server'] = self._global_headers.get('server', 'Aeros 2.0.0 (uvicorn)')  # change server header to Aeros
        self._global_headers = list(global_headers.items())  # convert dict to list of tuples for uvicorn

    def cache(self, timeout=None, key_prefix="view/%s", unless=None, forced_update=None,
              response_filter=None, query_string=False, hash_method=hashlib.md5, cache_none=False, ):
        """ A simple wrapper that forwards the cached() decorator to the internal Cache() instance.
        May be used as the normal @cache.cached() decorator."""

        def decorator(f):
            if self._cache is None:
                print('No cache specified in', self)
                return f

            @functools.wraps(f)
            @self._cache.cached(timeout=timeout, key_prefix=key_prefix, unless=unless, forced_update=forced_update,
                                response_filter=response_filter, query_string=query_string, hash_method=hash_method, cache_none=cache_none)
            async def decorated_function(*args2, **kwargs2):
                x = await f(*args2, **kwargs2)
                return x

            return decorated_function

        return decorator

    def clear_cache(self):
        """ Clears the WebServer instance cache. Use with caution!"""
        self._cache.clear()

    def _get_own_instance_path(self) -> str:
        """
        Retrieves the file and variable name of this instance to be used in the uvicorn CLI.

        Since uvicorn needs the application's file and global variable name for multicore execution, an
        instance needs to know it's own origin file and name. But since this class is not defined in the
        same file as it is called or defined from, this method searches for the correct module/file and
        evaluates it's instance name.

        .. warning::
            This method is a beta feature. Use with caution (good testing).

         """
        for i in range(10):
            try:
                frame = inspect.stack()[i][0].f_globals.items()
                for key, val in frame:
                    try:
                        if val == self:
                            path = f"{dict(frame)['__name__']}:{key}"
                            self.logger.debug(f"{self.__class__.__name__} resolved itself to \"{path}\"")
                            return path
                    except (RuntimeError, AttributeError, KeyError):
                        pass
            except IndexError:
                self.logger.critical(f"{self.__class__.__name__} is unable to find own instance file:name. Launching in single-thread mode!")
                return None

    def run_server(self,
                   host: str = None, port: int = None, log_level: int = None,  # overrides for __init__
                   access_log_file: str = None, access_log_to_std: bool = True,
                   soft_limit: int = 32, hard_limit: int = 42,
                   **kwargs
                   ) -> None:
        """ Generates the necessary config and runs the server instance. Possible keyword arguments are the same as supported by the
            `uvicorn.run()` method as they are passed into `Config(app, **kwargs)`. This method also configures features like caching
            and compression that are not default in Quart or Flask and unique to Aeros or require third-party modules to be configured.
        """
        if kwargs.get('suppress_deprecation_warning', False):
            del kwargs['suppress_deprecation_warning']
        else:
            self.logger.warning('The usage of run_server() is deprecated. Use run() instead.')  # delete, otherwise it gets into the config

        # Initialize extra features just in case the user replaced them with their own instances
        if issubclass(self._cache.__class__, Cache):
            self._cache.init_app(self)
            self.logger.info("Caching is enabled")
        else:
            self.logger.info("Caching is disabled")

        if issubclass(self._compression.__class__, Base):
            self._compression.init_app(self)
            self.logger.info("Compression is enabled")
        else:
            self.logger.info("Compression is disabled")

        # create uvicorn configuration ------------------------------------------------------------------------------------------------

        config = {
            'app': self,
            'host': host if host else self._host,
            'port': port if port else self._port,
            'headers': kwargs.get('headers', self._global_headers),

            'log_level': log_level if log_level else self.log_level,
            'access_log': bool(access_log_file) or access_log_to_std,

            'limit_concurrency': soft_limit + 1,
            'backlog': hard_limit,

            **kwargs
        }

        # set logging information
        self.logger.setLevel(log_level if log_level else self.log_level)  # re-set log level for instance logger if changed
        config['log_config'] = {  # logging configuration for uvicorn.run()
            'version': 1, 'disable_existing_loggers': True,
            'formatters': {
                'default': {'()': 'logging.Formatter', 'fmt': self.__log_format_std},
                'access_file': {'()': 'uvicorn.logging.AccessFormatter', 'fmt': '[%(asctime)s] %(client_addr)s | "%(request_line)s" | %(status_code)s'},
                'access_std': {'()': 'uvicorn.logging.AccessFormatter', 'fmt': '[%(asctime)s] ACCESS: %(client_addr)s | "%(request_line)s" | %(status_code)s'}
            },
            'handlers': {
                'default': {'formatter': 'default', 'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout'},
                'error': {'formatter': 'default', 'class': 'logging.StreamHandler', 'stream': 'ext://sys.stderr'}
            },
            'loggers': {
                'uvicorn': {'level': log_level, 'handlers': ['default']},
                'uvicorn.access': {'level': 'INFO', 'propagate': False, 'handlers': []}
            }
        }

        if access_log_to_std:
            config['log_config']['handlers']['access_std'] = {'formatter': 'access_std', 'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout'}
            config['log_config']['loggers']['uvicorn.access']['handlers'].append('access_std')
        if access_log_file:
            config['log_config']['handlers']['access_file'] = {'formatter': 'access_file', 'class': 'logging.FileHandler', 'filename': access_log_file}
            config['log_config']['loggers']['uvicorn.access']['handlers'].append('access_file')

            # try multi-core execution
        if config.get('workers', None):
            self.logger.debug(f"{self.__class__.__name__}.run_server() multi-core execution is a beta feature. You can also use uvicorn CLI directly.")
            instance_path = self._get_own_instance_path()
            if instance_path is not None:
                # if instance found, run multi-core by replacing instance with path
                config['app'] = instance_path
                self.logger.info(f"Starting in multi-thread mode...")
            else:
                # if instance not found, delete worker count and launch single-thread
                del config['workers']
                self.logger.info(f"Starting in single-thread mode...")

        uvicorn.run(**config)

    def run(self, *args, **kwargs):
        return self.run_server(*args, **kwargs, suppress_deprecation_warning=True)

    def route(self, *args, **kwargs):
        def new_route_decorator(func):
            new_func = EasyRequest()(func)  # inject EasyRequest into every function so that it is always available
            Quart.route(super(WebServer, self), *args, **kwargs)(new_func)  # route the new function to Quart.route

        return new_route_decorator
