from .task import Task


__all__ = (
    'Tube',
)


_FUNCS = [
    'put',
    'take',
    'touch',
    'ack',
    'release',
    'peek',
    'bury',
    'kick',
    'delete',
    'drop',
]


def build_func_name(tube_name, func_name):
    return 'queue.tube.{}:{}'.format(tube_name, func_name)


class Tube:
    __slots__ = (
        '_queue', '_name', '__funcs'
    )

    def __init__(self, queue, name):
        self._queue = queue
        self._name = name

        self.__funcs = {f: build_func_name(self._name, f) for f in _FUNCS}

    @property
    def queue(self):
        """
            Returns corresponding queue object

            :returns: :class:`asynctnt_queue.Tube` instance
        """
        return self._queue

    @property
    def conn(self):
        """
            Returns corresponding connection object

            :returns: :class:`asynctnt.Connection` instance
        """
        return self._queue._conn

    @property
    def name(self):
        """
            Tube name
        """
        return self._name

    def _create_task(self, body, *, task_cls=Task):
        """
            Creates Queue Task instance from Tarantool response body

            :param body: Response body
            :param task_cls: Class to instantiate
            :return: ``task_cls`` instance (by default
                :class:`asynctnt_queue.Task`)
        """
        return task_cls(self, body)

    async def put(self, data, *, pri=None, ttl=None, ttr=None, delay=None):
        """
            Puts data to the queue and returns a newly created Task

            :param data: Arbitrary task payload
            :param pri: Task priority (0 by default)
            :param ttl: Task time-to-live
            :param ttr: Task time-to-run
            :param delay: Task delay
            :return: Task instance
        """
        opts = {}
        if pri is not None:
            opts['pri'] = pri

        if ttl is not None:
            opts['ttl'] = ttl

        if ttr is not None:
            opts['ttr'] = ttr

        if delay is not None:
            opts['delay'] = delay

        args = (data, opts)
        res = await self.conn.call(self.__funcs['put'], args)
        return self._create_task(res.body)

    async def take(self, timeout=None):
        """
            Takes task from the queue, waiting the timeout if specified

            :param timeout: Seconds to wait for ready tasks
            :return: Task instance
        """
        args = None
        if timeout is not None:
            args = (timeout,)

        res = await self.conn.call(self.__funcs['take'], args)
        return self._create_task(res.body)

    async def touch(self, task_id, increment):
        """
            Update task ttl and/or ttr by increment value

            :param task_id: Task id
            :param increment: Seconds to add to ttr
            :return: Task instance
        """
        args = (task_id, increment)
        res = await self.conn.call(self.__funcs['touch'], args)
        return self._create_task(res.body)

    async def ack(self, task_id):
        """
            Ack task

            :param task_id: Task id
            :return: Task instance
        """
        args = (task_id,)
        res = await self.conn.call(self.__funcs['ack'], args)
        return self._create_task(res.body)

    async def release(self, task_id, *, delay=None):
        """
            Release task (return to queue) with delay if specified

            :param task_id: Task id
            :param delay: Time in seconds before task will become ready again
            :return: Task instance
        """
        opts = {}
        if delay is not None:
            opts['delay'] = delay
        args = (task_id, opts)
        res = await self.conn.call(self.__funcs['release'], args)
        return self._create_task(res.body)

    async def peek(self, task_id):
        """
            Get task without changing its state

            :param task_id: Task id
            :return: Task instance
        """

        args = (task_id,)
        res = await self.conn.call(self.__funcs['peek'], args)
        return self._create_task(res.body)

    async def bury(self, task_id):
        """
            Buries (disables) task

            :param task_id: Task id
            :return: Task instance
        """
        args = (task_id,)
        res = await self.conn.call(self.__funcs['bury'], args)
        return self._create_task(res.body)

    async def delete(self, task_id):
        """
            Deletes task from queue

            :param task_id: Task id
            :return: Task instance
        """
        args = (task_id,)
        res = await self.conn.call(self.__funcs['delete'], args)
        return self._create_task(res.body)

    async def kick(self, count):
        """
            Kick `count` tasks from queue

            :param count: Tasks count to kick
            :return: Number of tasks actually kicked
        """
        args = (count,)
        res = await self.conn.call(self.__funcs['kick'], args)
        return res.body[0]

    def statistics(self):
        """
            Return tube's statistics (identical to queue.statistics(tube_name))

            :return: Tube's statistics
        """
        return self._queue.statistics(self._name)
