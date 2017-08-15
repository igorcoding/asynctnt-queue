.. _asynctnt_queue-examples:

Examples
========

Basic Usage
-----------

Tarantool config:

.. code:: lua

    box.cfg {
        listen = '127.0.0.1:3301'
    }

    box.once('v1', function()
        box.schema.user.grant('guest', 'read,write,execute', 'universe')
    end)

    queue = require('queue')
    queue.create_tube('test_tube', 'fifottl')

Python code:

.. code:: python

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
