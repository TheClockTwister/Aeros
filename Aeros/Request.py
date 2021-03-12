"""
This module contains the wrapper for `Quart.request` that can be used inside web methods
"""

from quart import request
import functools


class EasyRequest:
    """ A helper class that makes request handling more uniform.

    All attributes are assessable via the same syntax, while with Flask.request
    or quart.request, you will have slightly different syntax when retrieving
    different request attributes, which can be very irritating and take much
    time debugging your code for missing parentheses or an await statement.

    .. hint::
        You only need to await attributes that need calculation, for example
        evaluating the request body, like `.json` or `.form`.

        .. code-block:: python

            headers = EasyRequest.headers
            params = EasyRequest.params
            form = await EasyRequest.form # requires time for calculation
            json = await EasyRequest.json # requires time for calculation
    """

    params: dict = ...
    """ The URL parameters like Flask.request.params. """

    headers: dict = ...
    """ The request headers like quart.request.headers. """

    cookies: dict = ...
    """ The request cookies like quart.request.cookies. """

    __quart_request: request = ...
    """ The quart.request. instance that is used in the current scope. """

    def __load(self):
        """ Loads the content of quart.request into this instance and returns it. """

        self.__quart_request = request
        self.params = dict(self.__quart_request.args)
        self.headers = dict(self.__quart_request.headers)
        self.cookies = dict(self.__quart_request.cookies)
        return self

    def __call__(self, f):
        """ Decorates an endpoint function to use the `EasyRequest` with, which makes
        `EasyRequest` available in that endpoint method.
        """

        @functools.wraps(f)
        async def decorated_function(*args2, **kwargs2):
            f.__globals__[self.__class__.__name__] = self.__class__().__load()
            return await f(*args2, **kwargs2)

        return decorated_function

    @property
    async def form(self):
        """ The request form data like quart.request.form. """
        return dict(await self.__quart_request.form)

    @property
    async def json(self):
        """ The request body data (as JSON) like quart.request.form.

        Be aware that in order for quart.request.get_json() to return
        a JSON dictionary, the `Content-Type` header must be set to
        `application/json`.
        """
        json = await self.__quart_request.get_json()
        return {} if json is None else json


if __name__ == '__main__':
    from Aeros import WebServer
    from quart import jsonify, render_template
    from time import strftime

    app = WebServer(__name__, host="0.0.0.0", port=80)  # init backend & web server
    app.template_folder = "./frontend/build/"
    app.static_folder = "./frontend/build/static/"


    @app.route("/")
    async def home():
        return await render_template("index.html")


    @app.route("/time/")
    async def current_time():
        print("Headers:", EasyRequest.headers)
        print("Params :", EasyRequest.params)
        print("Cookies:", EasyRequest.cookies)
        print("Form   :", await EasyRequest.form)
        print("JSON   :", await EasyRequest.json)
        return jsonify({"timestamp": strftime("%H:%M:%S")})


    app.run()  # run web server in this thread (endless mode)
