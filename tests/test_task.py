from asynctnt_queue import Queue, Tube, Task
from asynctnt_queue.task import Status
from tests import BaseTarantoolTestCase


class TaskTestCase(BaseTarantoolTestCase):
    def create_tube(self):
        q = Queue(self.conn)
        return q.tube("test_tube")

    def _data_obj(self):
        return {
            'key': 'value'
        }

    async def test__task_ack(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await t2.ack()
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.EXECUTED)
        self.assertEqual(t2.data, t.data)

    async def test__task_release(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await t2.release()
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.READY)
        self.assertEqual(t2.data, t.data)

    async def test__task_release_delay(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await t2.release(delay=5)
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.DELAYED)
        self.assertEqual(t2.data, t.data)

    async def test__task_bury(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await t2.bury()
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.BURIED)
        self.assertEqual(t2.data, t.data)

    async def test__task_peek(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await t2.peek()
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.TAKEN)
        self.assertEqual(t2.data, t.data)

    async def test__task_touch(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await t2.touch(1)
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.TAKEN)
        self.assertEqual(t2.data, t.data)

    async def test__task_delete(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await t2.delete()
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.EXECUTED)
        self.assertEqual(t2.data, t.data)

