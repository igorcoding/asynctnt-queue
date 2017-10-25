import enum

import asynctnt.log

from .exceptions import TaskEmptyError


__all__ = (
    'Status', 'Task'
)


class Status(enum.Enum):
    READY = 'r'
    TAKEN = 't'
    EXECUTED = '-'
    BURIED = '!'
    DELAYED = '~'


class Task:
    __slots__ = (
        '_tube', '_task_id', '_status', '_data'
    )

    def __init__(self, tube, tnt_tuple):
        self._tube = tube
        if tnt_tuple is None or len(tnt_tuple) == 0:  # pragma: nocover
            raise TaskEmptyError('Tarantool Queue task is empty')

        tnt_tuple = tnt_tuple[0]
        if tnt_tuple is None or len(tnt_tuple) == 0:  # pragma: nocover
            raise TaskEmptyError('Tarantool Queue task is empty')

        self._task_id = tnt_tuple[0]
        status = tnt_tuple[1]
        try:
            self._status = Status(status)
        except ValueError:  # pragma: nocover
            asynctnt.log.logger.warning(
                "unknown status '{}' in task_id = {}".format(
                    status, self._task_id))
            self._status = status
        self._data = tnt_tuple[2]

    @property
    def tube(self):
        """
            Task's tube
        """
        return self._tube

    @property
    def task_id(self):
        """
            Task id
        """
        return self._task_id

    @property
    def status(self):
        """
            Task status

            :returns: :class:`asynctnt_queue.Status` instance
        """
        return self._status

    @property
    def data(self):
        """
            Task data
        """
        return self._data

    def __repr__(self):
        return '<Task id={} status={}>'.format(self._task_id, self._status)

    async def touch(self, increment):
        """
            Update task ttl and/or ttr by increment value

            :param increment: Seconds to add to ttr
            :return: Task instance
        """
        return await self._tube.touch(self._task_id, increment)

    async def ack(self):
        """
            Ack task

            :return: Task instance
        """
        return await self._tube.ack(self._task_id)

    async def release(self, *, delay=None):
        """
            Release task (return to queue) with delay if specified

            :param delay: Time in seconds before task will become ready again
            :return: Task instance
        """
        return await self._tube.release(self._task_id, delay=delay)

    async def peek(self):
        """
            Get task without changing its state

            :return: Task instance
        """
        return await self._tube.peek(self._task_id)

    async def bury(self):
        """
            Buries (disables) task

            :return: Task instance
        """
        return await self._tube.bury(self._task_id)

    async def delete(self):
        """
            Deletes task from queue

            :return: Task instance
        """
        return await self._tube.delete(self._task_id)
