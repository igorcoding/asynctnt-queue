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
        """
            Queue constructor.

            :param conn:
                asynctnt connection (see
                `asynctnt <https://github.com/igorcoding/asynctnt>`__
                documentation)
            :param tube_cls:
                Tube class that is used for Tube creation (default is
                :class:`asynctnt_queue.Tube`)
        """
        assert isinstance(conn, asynctnt.Connection), \
            'conn must be asynctnt.Connection instance'
        self._conn = conn
        self._tube_cls = tube_cls
        self._tubes = {}

    @property
    def conn(self):
        """
            ``asynctnt`` connection

            :returns: :class:`asynctnt.Connection` instance
        """
        return self._conn

    def tube(self, name):
        """
            Returns tube by its name

            :param name: Tube name
            :returns: ``self.tube_cls`` instance
                (by default :class:`asynctnt_queue.Tube`)
        """
        if name in self._tubes:
            return self._tubes[name]

        assert name, 'Tube name must be specified'
        t = self._tube_cls(self, name)
        self._tubes[name] = t
        return t

    async def statistics(self, tube_name=None):
        """
            Returns queue statistics (coroutine)

            :param tube_name:
                If specified, statistics by a specific tube is returned,
                else statistics about all tubes is returned
        """
        args = None
        if tube_name is not None:
            args = (tube_name,)

        res = await self._conn.call('queue.statistics', args)
        if self._conn.version < (1, 7):
            return res.body[0][0]
        return res.body[0]
