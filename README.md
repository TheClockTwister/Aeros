![](images/Icon_header.png)

<p align="center">
  <img src="https://img.shields.io/pypi/pyversions/Aeros?label=Python%20Version&style=flat-square">
  <img src="https://img.shields.io/pypi/v/Aeros?label=PyPi%20Version&style=flat-square"/>
  <img src="https://img.shields.io/pypi/format/Aeros?label=PyPi%20Format&style=flat-square"/>
  <img src="https://img.shields.io/pypi/dm/Aeros?label=Downloads&style=flat-square"/>
  <img src="https://img.shields.io/github/repo-size/TheClockTwister/Aeros?label=Repo%20Size&style=flat-square">
</p>

# Aeros Documentation
Aeros is a production-grade ASGI (Asynchronous Server Gateway Interface) package
containing wrappers for widely used Web and API functions.

## Features
- High-performance web server
  - Async request handling
  - Supports multi-threading
- Production-grade ASGI (async WSGI)
- In-Python code API
- Can be run in a separate thread
- Easy Framework based on Flask/Quart


### Why use Aeros over Flask and Quart?
While Flask is one of the most popular and frequently used frameworks, it doesn't come
with a full WSGI server. Therefore, you will need an additional module like Waitress or
Gunicorn. Quart shares the same features as Flask, but you can get more performance out
of it, since it supports asynchronous request handling. But as for Flask, you will need
a WSGI (an ASGI in this case) to deploy your Quart app into production. The most popular
ASGI at the moment is called Hypercorn and is installed together with Quart.

But Hypercorn does only support deployment from console. Meaning, you will have to invoke
a start command like: `hypercorn <file>:<app_variable_name>` to start your server. This
makes it hard to deploy a multi-thread web server.

Aeros combines all the benefits from Quart and Hypercorn, while maintaining the in-Python
API, making it easy to create an application that can be run from custom code, not by shell.

A more detailed overview of pros and cons can be found here:

| Framework              | Async                   | Production-grade        | Easy to use             | In-Python API           | Callable from thread |
|:-----------------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|:---------------------:
| Flask                  |                         |                         | ![Yes](images/tick.png) | ![Yes](images/tick.png) | ?
| Flask + Waitress       |                         | ![Yes](images/tick.png) | ![Yes](images/tick.png) | ![Yes](images/tick.png) | ?
| Flask + Gunicorn       | ![Yes](images/tick.png) | ![Yes](images/tick.png) |                         | ![Yes](images/tick.png) | ?
| Quart                  | ![Yes](images/tick.png) |                         | ![Yes](images/tick.png) | ![Yes](images/tick.png) | ?
| Quart + Hypercorn      | ![Yes](images/tick.png) | ![Yes](images/tick.png) | ![Yes](images/tick.png) |                         | 
||    
| Aeros                  | ![Yes](images/tick.png) | ![Yes](images/tick.png) | ![Yes](images/tick.png) | ![Yes](images/tick.png) | ![Yes](images/tick.png)

### Getting started
This basic code snippet should get you ready for more. Remember that routed methods 
(the ones that are called on an HTTP endpoint) must be defined with `async def`, not `def`!

```python
from Aeros import WebServer
from Aeros.misc import jsonify

app = WebServer(__name__, host="0.0.0.0", port=80)


@app.route("/")
async def home():
    return jsonify({"response": "ok"})


if __name__ == '__main__':
    app.start("-w 2")  # worker threads (for more arguments see hypercorn documentation)
```

## Full Documentation

### Using sync methods in async methods
If you need to execute a synchronous method in an HTTP request handler and need to wait
for its response, you should use `sync_to_async` from `asgiref.sync`. This method can also
be imported from `Aeros.misc`:

```python
from Aeros.misc import sync_to_async
import time

@sync_to_async
def sync_method():
    time.sleep(2)
    return "ok"

@app.route("/")
async def home():
    status = sync_method()
    return jsonify({"response": status})
```

### Starting a server in a separate thread
Quart and Hypercorn don't allow server instances to be started from a non `__main__` thread.
Aeros however does. This code shows how:
```python
from Aeros import WebServer
from Aeros.threading import AdvancedThread
from threading import Thread
import time

app = WebServer(__name__, host="0.0.0.0", port=80, worker_threads=2)

...

if __name__ == '__main__':
    t = AdvancedThread(target=app.run_server, daemon=True)
    # OR
    t = Thread(target=app.run_server, daemon=True)

    t.start()
    time.sleep(120)
    t.stop() # only available in AdvancedThread, not in Thread
```


