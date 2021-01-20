Apyum
=====

[![Latest PyPI package version](https://badge.fury.io/py/apyum.svg)](https://pypi.org/project/apyum)  
Adapter for Celery that implements JSON-RPC 2.0 protocol.

Key Features
------------
- Turns existing Celery implementation into a JSON RPC api
- Simple to run
- Implements JSON-RPC 2.0 protocol. (see https://www.jsonrpc.org)
- Support asyncio

Getting started
---------------
Create a yml config file (for example **settings.yaml**):
```yaml
celery:
  broker_url: "amqp://guest:guest@localhost:5672//"
  result_backend: "rpc://"
  result_persistent: False
  ...
logging:
  ...
 ```

The *celery* section is to be written as described by the Celery configuration (see https://docs.celeryproject.org/en/stable/userguide/configuration.html).  
The *logging* section is optional and can be customized as described by the Python logging manual (see https://docs.python.org/3/library/logging.config.html).  

To start Apyum launch standalone:
```sh
apyum settings.yml
```
This starts Apyum listening to 8080 port. For change listening port user parameter --port or to listen in a unix socket use parameter --path  

Or start with gunicorn:
```sh
APYUM_SETTINGS=settings.yml gunicorn apyum.main:create --bind localhost:5000 --worker-class aiohttp.GunicornWebWorker --worker 4
```

Calling service example
-----------------------
Suppose we have defined some Celery tasks as **myapp.tasks** python module in a external worker like this:
(tasks.py)
```python
@app.task
def example_task_x(a, b, c):
    ...

@app.task
def example_task_y(a, b, c):
    ...
```
For running by JSON-RPC call we must send POST to http://localhost:8080/myapp/tasks with body:
```json
{ "jsonrpc": "2.0", "method": "example_task_x", "params": { "a": 5, "b": 3, "c":1}, "id": "1" }
```
or
```json
{ "jsonrpc": "2.0", "method": "example_task_x", "params": [ 5, 3, 1], "id": "1" }
```
or can be called on root by:
```json
{ "jsonrpc": "2.0", "method": "myapp.tasks.example_task_x", "params": [ 5, 3, 1], "id": "1" }
```
The endpoints return response if have it. Also batch calls are supported:
```json
[
  { "jsonrpc": "2.0", "method": "myapp.tasks.example_task_x", "params": [ 5, 3, 1], "id": "1" },
  { "jsonrpc": "2.0", "method": "myapp.tasks.example_task_y", "params": [ 1, 2, 1], "id": "2" },
  { "jsonrpc": "2.0", "method": "myapp.tasks.example_task_y", "params": [ 6, 1, 4], "id": "3" }
]
```
See JSON-RPC specification for more details.  

Installation
------------
It's very simple to install Apyum:
```sh
pip install apyum
```

To Do
-----
- More tests
- Autentication requests
- Insert an api documentation (like https://open-rpc.org)
- Documentation and examples

Requirements
------------
- Python >= 3.8
- Celery 5

License
-------
`apyum` is offered under the Apache 2 license.

Source code
-----------
The latest developer version is available in a GitHub repository:
<https://github.com/aiselis/apyum>