from quart import Quart as Original
from .asgi import ASGIHTTPConnection


class Quart(Original):
    asgi_http_class = ASGIHTTPConnection
