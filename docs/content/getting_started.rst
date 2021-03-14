.. _localhost: http://127.0.0.1/
.. _flask_routes https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing

.. admonition:: Know what to ask

    Aeros uses methods from the quart module, which itself copies the syntax of flask.
    You may treat an ``Aeros.WebServer`` instance just like a ``quart.Quart`` instance.

    **Most of the Flask documentation also applies to Quart and therefore to Aeros. Use it!**

Prerequisites
===========================================================
- install the Aeros module to your Python interpreter of choice:

    .. code-block::

        pip install -U Aeros

- open up your favourite IDE and create a new project


The bare minimum
===========================================================
The following code block sets-up a very basic web server that can be accessed via HTTP for example by your browser:

    .. code-block::

        from Aeros import WebServer

        app = WebServer(__name__)

        @app.route("/")
        async def just_say_hello():
            return "Hi, I am your new backend :)"

        app.run()

You should now be able to access localhost_ in your browser and get a response.


Adding endpoints
-----------------------------------------------------------
If you wish to host multiple "pages", you can just add another function and decorate it with the
``@app.route()`` decorator:

.. code-block::

        from Aeros import WebServer

        app = WebServer(__name__)

        @app.route("/")
        async def just_say_hello():
            return "Hi, I am your new backend :)"

        @app.route("/goodbye")
        async def say_bye():
            return "Good bye, friend :("

        app.run()


Implementing logic
-----------------------------------------------------------
When implementing logic to answer your requests, you need to pay close attention as to what you
are executing. Since Aeros runs asynchronous, one needs to await certain operations. This is the
case for asynchronous operations like ``render_template()`` which renders an HTML page. But since
Aeros has to look up the contents from your hard disk first, we have to wait 1 or 2 milliseconds
before it can send the answer. That's why we write ``await`` in front of it.

.. code-block::

        from Aeros import WebServer
        from quart import render_template

        app = WebServer(__name__)

        @app.route("/")
        async def homepage():
            return await render_template('index.html')

        app.run()

.. warning::

    Make sure to always import methods from the ``quart`` module, not ``flask``, since Flask runs synchronous
    and therefore does not work with an asynchronous web server. Fore more information, see
    `What's async programming <https://medium.com/velotio-perspectives/an-introduction-to-asynchronous-programming-in-python-af0189a88bbb>`_
