<p align="center">
  <img src="https://img.shields.io/pypi/pyversions/Aeros?label=Python%20Version&style=flat-square">
  <img src="https://img.shields.io/pypi/v/Aeros?label=PyPi%20Version&style=flat-square"/>
  <img src="https://img.shields.io/pypi/format/Aeros?label=PyPi%20Format&style=flat-square"/>
  <img src="https://img.shields.io/pypi/dm/Aeros?label=Downloads&style=flat-square"/>
  <img src="https://img.shields.io/github/repo-size/TheClockTwister/Aeros?label=Repo%20Size&style=flat-square">
</p>

# About Aeros
[Aeros](https://pypi.org/project/Aeros/) is a production-grade ASGI (Asynchronous Server Gateway Interface) package
containing wrappers for widely used Web and API functions. It combines all the benefits from Quart and Hypercorn,
while maintaining the in-Python API, making it easy to create an application that can be run from custom code, not
by shell. Additionally, Aeros adds powerful wrappers, that make complex features easy to code and implement.

**In the end, it is meant to provide an API for web applications that is as intuitive as possible.**

## Features
- High-performance web server
    - Async request handling
    - Supports multi-threading
- Production-grade ASGI (async WSGI)
    - Can be run in a separate thread
    - Easy Framework based on Flask/Quart
- Native HTTP features
    - Native server-side caching
    - Native gzip compression
    - Custom global headers (like CORS etc.)
- EasyRequest handler (improvement of Flask.request)
- Full In-Python code API


## Aeros over Flask and Quart?
While Flask is one of the most popular and frequently used frameworks, it doesn't come
with a full WSGI server. Therefore, you will need an additional module like Waitress or
Gunicorn. Quart shares the same features as Flask, but you can get more performance out
of it, since it supports asynchronous request handling. But as for Flask, you will need
a WSGI (an ASGI in this case) to deploy your Quart app into production. The most popular
ASGI at the moment is called Hypercorn and is installed together with Quart.

But Hypercorn does only support deployment from console. Meaning, you will have to invoke
a start command like: `hypercorn <file>:<app_variable_name>` to start your server. This
makes it hard to deploy a multi-thread web server and requires a ton of efford to debug
and control and monitor the web server instance of your application.
