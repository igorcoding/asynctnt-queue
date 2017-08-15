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
        if tnt_tuple is None or len(tnt_tuple) == 0:
            raise TaskEmptyError('Tarantool Queue task is empty')

        tnt_tuple = tnt_tuple[0]
        if tnt_tuple is None or len(tnt_tuple) == 0:
            raise TaskEmptyError('Tarantool Queue task is empty')

        self._task_id = tnt_tuple[0]
        status = tnt_tuple[1]
        try:
            self._status = Status(status)
        except ValueError:
            asynctnt.log.logger.warning(
                "unknown status '{}' in task_id = {}".format(
                    status, self._task_id))
            self._status = status
        self._data = tnt_tuple[2]

    @property
    def tube(self):
        return self._tube

    @property
    def task_id(self):
        return self._task_id

    @property
    def status(self):
        return self._status

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return '<Task id={} status={}>'.format(self._task_id, self._status)

    def touch(self, increment):
        return self._tube.touch(self._task_id, increment)

    def ack(self):
        return self._tube.ack(self._task_id)

    def release(self, *, delay=None):
        return self._tube.release(self._task_id, delay=delay)

    def peek(self):
        return self._tube.peek(self._task_id)

    def bury(self):
        return self._tube.bury(self._task_id)

    def delete(self):
        return self._tube.delete(self._task_id)
