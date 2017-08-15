class QueueError(Exception):
    """
        Base QueueError exception
    """
    pass


class TaskEmptyError(QueueError):
    """
        Raised when Tarantool responds with empty body for task
    """
    pass
