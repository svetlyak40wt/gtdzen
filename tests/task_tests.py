import os
from pdb import set_trace
from unittest import TestCase
from gtdzen import GTD

TEST_DB = 'testsuite.sqlite'

class TaskTests(TestCase):
    def __init__(self, *args, **kwargs):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.gtd = GTD(TEST_DB)
        super(TaskTests, self).__init__(*args, **kwargs)

    def setUp(self):
        self.gtd.removeAll()

    def testAddTask(self):
        title = u'Test title'
        note = u'Simple note'
        tags = 'one, two'
        priority = 10

        task = self.gtd.addTask(title = u'Test title', note = u'Simple note', tags = [u'one', u'two'], priority = 10)
        self.assert_(task)
        self.assertEqual(title, task.title)
        self.assertEqual(note, task.note)
        self.assertEqual(2, len(task.tags))
        self.assertEqual(priority, task.priority)

    def testAddTwoTasksWithDefaults(self):
        task1 = self.gtd.addTask(title = u'First')
        task2 = self.gtd.addTask(title = u'Second')

        self.assertNotEqual(task1.title, task2.title)
        self.assertEqual(None, task1.note)
        self.assertEqual(None, task2.note)
        self.assertEqual(1, task1.priority)
        self.assertEqual(1, task2.priority)
        self.assertEqual([], task1.tags)
        self.assertEqual([], task2.tags)

    def testGetTasks(self):
        task1 = self.gtd.addTask(title = u'First',  priority = 1)
        task2 = self.gtd.addTask(title = u'Second', priority = 2)

        tasks = self.gtd.getTasks()
        self.assertEqual(2, len(tasks))
        self.assertEqual(task2, tasks[0])
        self.assertEqual(task1, tasks[1])

    def testGetTags(self):
        self.gtd.addTask(title = u'First', tags = [u'one', u'two', u'three'])

        tags = self.gtd.getTags()
        tag_titles = [t.title for t in tags]

        self.assertEqual(u'one',   tag_titles[0])
        self.assertEqual(u'three', tag_titles[1])
        self.assertEqual(u'two',   tag_titles[2])

