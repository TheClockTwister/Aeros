![](Icon_header.png)

# Aeros Documentation
Aeros is a production-grade ASGI (Asynchronous Server Gateway Interface) package
containing wrappers for widely used Web and API functions.

## Features
- High-performance web server
  - Async request handling
  - Supports multi-threading
- Production-grade ASGI (async WSGI)
- In-Python code API
- Easy Framework based on Flask/Quart


## Why use Aeros over Flask and Quart?
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

| Framework              | Async | Production-grade  | Easy to use       | In-Python API
|:-----------------------|:-----:|:-----------------:|:-----------------:|:-------------:
| Flask                  | No    | No                | No                 | Yes
| Flask + Waitress       | No    | Yes                 | No                | Yes
| Flask + Gunicorn       | Yes     | Yes                | No                 | Yes
| Quart                  | Yes     | No                | Yes                 | No
| Quart + Hypercorn      | Yes     | Yes                | Yes                 | No
||    
| Aeros                  | Yes     | Yes                | Yes                 | Yes

## Getting started
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



## Using sync methods in async methods
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
