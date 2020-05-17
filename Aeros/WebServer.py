"""
Main web server instance
"""
import argparse
import warnings
import inspect
import ssl
from typing import Union, Dict

from quart import Quart
from Aeros.patches.hypercorn.run import run
from Aeros.patches.hypercorn.Config import Config


class WebServer(Quart):
    """ This is the main server class which extends a standard Flask class by a bunch of features and major
    performance improvements. It extends the Quart class, which by itself is already an enhanced version of
    the Flask class. This class however allows production-grade  deployment using the hypercorn WSGI server
    as production server. But instead of calling the hypercorn command via the console, it can be started
    directly from the Python code itself, making it easier to integrate in higher-level scripts and
    applications without calling os.system() od subprocess.Popen(). """

    def __init__(self, import_name: str, host: str = None, port: int = None, include_server_header: bool = True,
                 hypercorn_arg_string: str = "", worker_threads: int = 1, logging_level: Union[int, str] = "INFO",
                 global_headers: Dict[str, str] = {},
                 *args, **kwargs):

        super().__init__(import_name, *args, **kwargs)

        self.logger.setLevel(logging_level)
        self._host, self._port = host, port
        self._global_headers = global_headers
        self._hypercorn_arg_string = hypercorn_arg_string
        self._worker_threads = worker_threads
        self._include_server_header = include_server_header

    def _get_own_instance_path(self):
        """ DEPRECATED!
         Since hypercorn needs the application's file and global variable name, an instance needs to know
         it's own origin file and name. But since this class is not defined in the same file as it is called
         or defined from, this method searches for the correct module/file and evaluates it's instance name. """
        self.logger.warning("_get_own_instance_path() is deprecated!")
        for i in range(10):
            try:
                frame = inspect.stack()[i][0].f_globals.items()
                for key, val in frame:
                    try:
                        if val == self:
                            return f"{dict(frame)['__name__']}:{key}"
                    except (RuntimeError, AttributeError, KeyError):
                        pass
            except:
                pass
        raise Exception("QuartServer() is unable to find own instance file:name")

    def run_server(self) -> None:
        """ This method is very similar to hypercorn.__main___ and runs a Quart application like from the command prompt. """

        def _convert_verify_mode(value: str) -> ssl.VerifyMode:
            try:
                return ssl.VerifyMode[value]
            except KeyError:
                raise argparse.ArgumentTypeError("Not a valid verify mode")

        sentinel = object()
        parser = argparse.ArgumentParser()
        parser.add_argument("--access-log", default=sentinel)
        parser.add_argument("--access-logfile", default=sentinel)
        parser.add_argument("--access-logformat", default=sentinel)
        parser.add_argument("--backlog", type=int, default=sentinel)
        parser.add_argument("-b", "--bind", dest="binds", default=[], action="append", )
        parser.add_argument("--ca-certs", default=sentinel)
        parser.add_argument("--certfile", default=sentinel)
        parser.add_argument("--cert-reqs", type=int, default=sentinel)
        parser.add_argument("--ciphers", default=sentinel)
        parser.add_argument("-c", "--config", default=None)
        parser.add_argument("--debug", action="store_true", default=sentinel)
        parser.add_argument("--error-log", default=sentinel)
        parser.add_argument("--error-logfile", "--log-file", dest="error_logfile", default=sentinel)
        parser.add_argument("-g", "--group", default=sentinel, type=int)
        parser.add_argument("-k", "--worker-class", dest="worker_class", default=sentinel)
        parser.add_argument("--keep-alive", default=sentinel, type=int)
        parser.add_argument("--keyfile", default=sentinel)
        parser.add_argument("--insecure-bind", dest="insecure_binds", default=[], action="append")
        parser.add_argument("--log-config", default=sentinel)
        parser.add_argument("--log-level", default="info")
        parser.add_argument("-p", "--pid", default=sentinel)
        parser.add_argument("--quic-bind", dest="quic_binds", default=[], action="append")
        parser.add_argument("--reload", action="store_true", default=sentinel)
        parser.add_argument("--root-path", default=sentinel)
        parser.add_argument("--statsd-host", default=sentinel)
        parser.add_argument("--statsd-prefix", default="")
        parser.add_argument("-m", "--umask", default=sentinel, type=int)
        parser.add_argument("-u", "--user", default=sentinel, type=int)
        parser.add_argument("-w", "--workers", dest="workers", default=sentinel, type=int)
        parser.add_argument("--verify-mode", type=_convert_verify_mode, default=sentinel)

        args = self._hypercorn_arg_string.split(" ").remove("") if "" in self._hypercorn_arg_string.split(" ") else self._hypercorn_arg_string.split(" ")
        args = parser.parse_args(args)
        config = Config(self._global_headers)

        config.loglevel = args.log_level

        if args.access_logformat is not sentinel:
            config.access_log_format = args.access_logformat
        if args.access_log is not sentinel:
            warnings.warn("The --access-log argument is deprecated, use `--access-logfile` instead", DeprecationWarning, )
            config.accesslog = args.access_log
        if args.access_logfile is not sentinel:
            config.accesslog = args.access_logfile
        if args.backlog is not sentinel:
            config.backlog = args.backlog
        if args.ca_certs is not sentinel:
            config.ca_certs = args.ca_certs
        if args.certfile is not sentinel:
            config.certfile = args.certfile
        if args.cert_reqs is not sentinel:
            config.cert_reqs = args.cert_reqs
        if args.ciphers is not sentinel:
            config.ciphers = args.ciphers
        if args.debug is not sentinel:
            config.debug = args.debug
        if args.error_log is not sentinel:
            warnings.warn("The --error-log argument is deprecated, use `--error-logfile` instead", DeprecationWarning, )
            config.errorlog = args.error_log
        if args.error_logfile is not sentinel:
            config.errorlog = args.error_logfile
        if args.group is not sentinel:
            config.group = args.group
        if args.keep_alive is not sentinel:
            config.keep_alive_timeout = args.keep_alive
        if args.keyfile is not sentinel:
            config.keyfile = args.keyfile
        if args.log_config is not sentinel:
            config.logconfig = args.log_config
        if args.pid is not sentinel:
            config.pid_path = args.pid
        if args.root_path is not sentinel:
            config.root_path = args.root_path
        if args.reload is not sentinel:
            config.use_reloader = args.reload
        if args.statsd_host is not sentinel:
            config.statsd_host = args.statsd_host
        if args.statsd_prefix is not sentinel:
            config.statsd_prefix = args.statsd_prefix
        if args.umask is not sentinel:
            config.umask = args.umask
        if args.user is not sentinel:
            config.user = args.user
        if args.worker_class is not sentinel:
            config.worker_class = args.worker_class
        config.workers = self._worker_threads
        if args.workers is not sentinel:
            config.workers = args.workers
        if self._host and self._port:
            config.bind = [f'{self._host}:{self._port}']
        if len(args.binds) > 0:
            config.bind = args.binds
        if len(args.insecure_binds) > 0:
            config.insecure_bind = args.insecure_binds
        if len(args.quic_binds) > 0:
            config.quic_bind = args.quic_binds

        config.include_server_header = self._include_server_header

        run(self, config)
