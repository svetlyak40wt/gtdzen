from unittest import TestCase
from gtdzen import *

class TaskTests(TestCase):
    def testAddTask(self):
        title = u'Test title'
        note = u'Simple note'
        tags = 'one, two'
        priority = 10

        task = add_task(title = u'Test title', note = u'Simple note', tags = 'one, two', priority = 10)
        self.assert_(task)
        self.assertEqual(title, task.title)
        self.assertEqual(note, task.note)
        self.assertEqual(2, len(task.tags))
        self.assertEqual(priority, task.priority)
