# asynctnt-queue

[![Build Status](https://travis-ci.org/igorcoding/asynctnt-queue.svg?branch=master)](https://travis-ci.org/igorcoding/asynctnt-queue)
[![PyPI](https://img.shields.io/pypi/v/asynctnt-queue.svg)](https://pypi.python.org/pypi/asynctnt-queue)


asynctnt-queue is a python/asyncio bindings library for
[tarantool-queue](https://github.com/tarantool/queue) package in
[Tarantool Database](https://tarantool.org/), integrated with [asynctnt](https://github.com/igorcoding/asynctnt) module.


## Documentation

Documentation is available [here](https://igorcoding.github.io/asynctnt-queue).


## Installation
Use pip to install:
```bash
$ pip install asynctnt-queue
```

## Basic Usage

Tarantool config:

```lua
box.cfg {
    listen = '127.0.0.1:3301'
}

box.once('v1', function()
    box.schema.user.grant('guest', 'read,write,execute', 'universe')
end)

queue = require('queue')
queue.create_tube('test_tube', 'fifottl')
```

Python code:
```python
import asyncio
import asynctnt
import asynctnt_queue


async def run():
    conn = asynctnt.Connection(host='127.0.0.1', port=3301)
    await conn.connect()
    
    queue = asynctnt_queue.Queue(conn)
    test_tube = queue.tube('test_tube')
    
    # Add a task to queue
    task = await test_tube.put({
        'key': 'value'
    })
    
    print('Task id: {}'.format(task.task_id))
    print('Task status: {}'.format(task.status))
    
    # Retrieve a task from queue
    task = await test_tube.take(1)
    
    # ... do some work with task
    
    await task.ack()
    await conn.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
```


## References

1. [Tarantool](https://tarantool.org) - in-memory database and application server.
2. [asynctnt](https://github.com/igorcoding/asynctnt) - fast Tarantool database connector for Python/asyncio
3. [aiotarantool](https://github.com/shveenkov/aiotarantool) - alternative Python/asyncio connector 


