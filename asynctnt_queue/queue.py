import asynctnt

from .tube import Tube

__all__ = (
    'Queue',
)


class Queue:
    __slots__ = (
        '_conn', '_tube_cls', '_tubes'
    )

    def __init__(self,
                 conn: asynctnt.Connection,
                 tube_cls=Tube):
        assert isinstance(conn, asynctnt.Connection), \
            'conn must be asynctnt.Connection instance'
        self._conn = conn
        self._tube_cls = tube_cls
        self._tubes = {}

    @property
    def conn(self):
        return self._conn

    def tube(self, name):
        if name in self._tubes:
            return self._tubes[name]

        assert name, 'Tube name must be specified'
        t = self._tube_cls(self, name)
        self._tubes[name] = t
        return t

    async def statistics(self, tube_name=None):
        args = None
        if tube_name is not None:
            args = (tube_name,)

        res = await self._conn.call('queue.statistics', args)
        if self._conn.version < (1, 7):
            return res.body[0][0]
        return res.body[0]
