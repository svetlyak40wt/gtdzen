import os
from unittest import TestCase
from gtdzen import GTD

TEST_DB = 'testsuite.sqlite'

class TaskTests(TestCase):
    def __init__(self, *args, **kwargs):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.gtd = GTD(TEST_DB)
        super(TaskTests, self).__init__(*args, **kwargs)

    def testAddTask(self):
        title = u'Test title'
        note = u'Simple note'
        tags = 'one, two'
        priority = 10

        task = self.gtd.addTask(title = u'Test title', note = u'Simple note', tags = ['one', 'two'], priority = 10)
        self.assert_(task)
        self.assertEqual(title, task.title)
        self.assertEqual(note, task.note)
        self.assertEqual(2, len(task.tags))
        self.assertEqual(priority, task.priority)
