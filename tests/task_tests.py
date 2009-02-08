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

    def testAddTwoTasksWithSameTag(self):
        self.gtd.addTask(title = u'First', tags = [u'today'])
        self.gtd.addTask(title = u'Second', tags = [u'today'])
        self.assertEqual(2, len(self.gtd.getTasks()))

    def testGetRelatedTags(self):
        self.gtd.addTask(title = u'First', tags = [u'today', u'home', u'1 minute'])
        self.gtd.addTask(title = u'Second', tags = [u'today', u'work', u'call'])

        self.assertEqual(
            [u'1 minute', u'call', u'home', u'work'],
            [t.title for t in self.gtd.getTagsRelated(u'today')])

        self.assertEqual(
            [u'1 minute', u'today'],
            [t.title for t in self.gtd.getTagsRelated(u'home')])

        self.assertEqual(
            [u'today'],
            [t.title for t in self.gtd.getTagsRelated([u'home', u'1 minute'])])

    def testGetFilteredTasks(self):
        task1 = self.gtd.addTask(title = u'First',  tags = [u'home', u'1 minute'], priority = 1)
        task2 = self.gtd.addTask(title = u'Second', tags = [u'work', u'1 minute'], priority = 5)
        task3 = self.gtd.addTask(title = u'Third', tags = [u'work', u'long'], priority = 3)

        tasks = self.gtd.getTasks(u'1 minute')
        self.assertEqual(2, len(tasks))
        self.assertEqual(task2, tasks[0])
        self.assertEqual(task1, tasks[1])

        tasks = self.gtd.getTasks(u'work')
        self.assertEqual(2, len(tasks))
        self.assertEqual(task2, tasks[0])
        self.assertEqual(task3, tasks[1])

        tasks = self.gtd.getTasks([u'work', u'long'])
        self.assertEqual(1, len(tasks))
        self.assertEqual(task3, tasks[0])

    def testModify(self):
        task1 = self.gtd.addTask(title = u'First',  tags = [u'home', u'1 minute'], priority = 1)
        task1.priority = 5
        task1.setTags([u'work', u'about hour'])

        task = self.gtd.getTaskById(task1.id)
        self.assertEqual(5, task.priority)
        self.assertEqual(2, len(task.tags))
        self.assertEqual(u'work',       task.tags[0].title)
        self.assertEqual(u'about hour', task.tags[1].title)

