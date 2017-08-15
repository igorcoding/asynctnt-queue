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
        return self._queue

    @property
    def conn(self):
        return self._queue._conn

    @property
    def name(self):
        return self._name

    def create_task(self, body, *, task_cls=Task):
        return task_cls(self, body)

    async def put(self, data, *, pri=None, ttl=None, ttr=None, delay=None):
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
        return self.create_task(res.body)

    async def take(self, timeout=None):
        args = None
        if timeout is not None:
            args = (timeout,)

        res = await self.conn.call(self.__funcs['take'], args)
        return self.create_task(res.body)

    async def touch(self, task_id, increment):
        args = (task_id, increment)
        res = await self.conn.call(self.__funcs['touch'], args)
        return self.create_task(res.body)

    async def ack(self, task_id):
        args = (task_id,)
        res = await self.conn.call(self.__funcs['ack'], args)
        return self.create_task(res.body)

    async def release(self, task_id, *, delay=None):
        opts = {}
        if delay is not None:
            opts['delay'] = delay
        args = (task_id, opts)
        res = await self.conn.call(self.__funcs['release'], args)
        return self.create_task(res.body)

    async def peek(self, task_id):
        args = (task_id,)
        res = await self.conn.call(self.__funcs['peek'], args)
        return self.create_task(res.body)

    async def bury(self, task_id):
        args = (task_id,)
        res = await self.conn.call(self.__funcs['bury'], args)
        return self.create_task(res.body)

    async def kick(self, count):
        args = (count,)
        res = await self.conn.call(self.__funcs['kick'], args)
        return res.body[0]

    async def delete(self, task_id):
        args = (task_id,)
        res = await self.conn.call(self.__funcs['delete'], args)
        return self.create_task(res.body)

    async def drop(self):
        res = await self.conn.call(self.__funcs['drop'])
        return res

    def statistics(self):
        return self._queue.statistics(self._name)
