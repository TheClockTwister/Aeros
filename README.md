![](Icon_header.png)

# Aeros Documentation
Aeros is a package containing wrappers for widely used Web and API functions.
The whole package is based on Quart/Flask.

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
