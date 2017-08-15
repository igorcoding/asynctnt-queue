from asynctnt_queue import Queue, Tube
from tests import BaseTarantoolTestCase


class QueueTestCase(BaseTarantoolTestCase):
    async def test__queue_create(self):
        q = Queue(self.conn)
        self.assertEqual(q.conn, self.conn, 'conn valid')

    def test__queue_get_tube(self):
        q = Queue(self.conn)
        tube = q.tube('test_tube')

        self.assertEqual(tube.name, 'test_tube', 'name valid')
        self.assertIsInstance(tube, Tube, 'tube valid type')
        self.assertEqual(tube.conn, self.conn, 'conn valid')

    async def test__queue_statistics(self):
        q = Queue(self.conn)
        res = await q.statistics()
        self.assertIsNotNone(res)
        self.assertIn('test_tube', res)
