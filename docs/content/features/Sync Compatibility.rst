Sync Compatibility
===========================================================

Since Aeros is built on `Quart <https://pypi.org/project/Quart/>`_, which
is an asynchronous implemtation / re-implementation of the more commonly
known framework `Flask <https://pypi.org/project/Flask/>`_, endpoint
functions must be asynchronous.

As an improvement over Quart, Aeros will recognize the registration of synchronous
functions and try to "convert" them to asynchronous coroutines, if possible. Of
cause, there is a bit more to it than simple "conversion", which is why this feature
should be used with care. It is meant as a backup for those who don't yet know how
to implement asynchronous functions or those who forget about it. Instead of getting
an HTTP 500 response code and an exception, your app will at least have a chance.

A brief example of how this works can be seen in the following example code snippet:

    .. code-block::

        from aeros import WebServer

        app = WebServer(__name__)

        @app.route("/sync")
        def i_am_sync(): # NOTE: no "async def"
            return "SYNC :("

        @app.route("/async")
        async def i_am_async(): # NOTE: "async def"
            return "ASYNC :)"

        app.run()


    .. warning:: Available since version 2.0.0

        You should always write asynchronous functions for endpoints. This feature is
        meant as a backup, not a caretaker to rely on.
