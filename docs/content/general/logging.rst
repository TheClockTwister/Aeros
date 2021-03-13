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
            log_level=DEBUG, # set your desired logging level
            access_log_to_std=True, # Set False if you don't want the access log in stdout
            access_log_file='access.log', # Specify if you want to log access to a file
            traceback=True # Set False if you do not want tracebacks written to stderr
        )

    .. admonition:: Available since version 2.0.0

        The behaviour described above is available for versions >= 2.0.0.
