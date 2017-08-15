class QueueError(Exception):
    pass


class TaskEmptyError(QueueError):
    pass
