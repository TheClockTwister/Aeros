Logging
===========================================================

By default, all output will be written to **stdout**,
except tracebacks, which will be written to **stderr**.

You can adjust the logging behaviour by using keywords on `Webserver.run()`
as described in the following example code snippet:

    .. code-block::

        from Aeros import WebServer

        app = WebServer(__name__)

        @app.route("/")
        async def just_say_hello():
            return "Hi, I am your new backend :)"

        app.run(
            log_level=logging.DEBUG, # set logging level (default: INFO)
            log_to_std=False, # print logs to console (default: True)
            access_log_to_std=False, # print access logs to console (default: True)
            default_log_file='log.log', # if specified, write server logs to file
            access_log_file='access.log', # if specified, write access logs to file
            traceback=False, # log tracebacks if exceptions occur (default: True)
            color=True # colored terminal output (default: True) (doesn't affect files)
        )

    .. admonition:: Available since version 2.0.0

        The behaviour described above is available for versions >= 2.0.0.
