from asynctnt_queue import Queue, Tube, Task
from asynctnt_queue.task import Status
from tests import BaseTarantoolTestCase


class TubeTestCase(BaseTarantoolTestCase):
    def create_tube(self):
        q = Queue(self.conn)
        return q.tube("test_tube")

    def _data_obj(self):
        return {
            'key': 'value'
        }

    async def test__tube_put(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        self.assertIsNotNone(t)
        self.assertIsInstance(t, Task)
        self.assertEqual(t.status, Status.READY)
        self.assertEqual(t.task_id, 0)  # first task has id = 0
        self.assertEqual(t.data, self._data_obj())

    async def test__tube_take(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        taken_t = await tube.take()
        self.assertEqual(taken_t.task_id, t.task_id, 'task id equal')
        self.assertEqual(taken_t.status, Status.TAKEN)
        self.assertDictEqual(taken_t.data, t.data)

    async def test__tube_ack(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await tube.ack(t2.task_id)
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.EXECUTED)
        self.assertEqual(t2.data, t.data)

    async def test__tube_release(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await tube.release(t2.task_id)
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.READY)
        self.assertEqual(t2.data, t.data)

    async def test__tube_release_delay(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await tube.release(t2.task_id, delay=5)
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.DELAYED)
        self.assertEqual(t2.data, t.data)

    async def test__tube_bury(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await tube.bury(t2.task_id)
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.BURIED)
        self.assertEqual(t2.data, t.data)

    async def test__tube_peek(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await tube.peek(t2.task_id)
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.TAKEN)
        self.assertEqual(t2.data, t.data)

    async def test__tube_touch(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await tube.touch(t2.task_id, 1)
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.TAKEN)
        self.assertEqual(t2.data, t.data)

    async def test__tube_delete(self):
        tube = self.create_tube()
        t = await tube.put(self._data_obj())
        t2 = await tube.take()
        t2 = await tube.delete(t2.task_id)
        self.assertEqual(t2.task_id, t.task_id)
        self.assertEqual(t2.status, Status.EXECUTED)
        self.assertEqual(t2.data, t.data)

    async def test__tube_statistics(self):
        tube = self.create_tube()
        res = await tube.statistics()
        self.assertIsNotNone(res)

