# This code is licensed under the New BSD License
# 2009, Alexander Artemenko <svetlyak.40wt@gmail.com>
# For other contacts, visit http://aartemenko.com

import os
from pdb import set_trace
from unittest import TestCase
from gtdzen import GTD
from gtdzen.exceptions import *

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

    def testGetTasksWithoutTags(self):
        task1 = self.gtd.addTask(title = u'First',  tags = [u'home', u'1 minute'], priority = 1)
        task2 = self.gtd.addTask(title = u'Second', tags = [u'work', u'1 minute'], priority = 5)
        task3 = self.gtd.addTask(title = u'Third', tags = [u'work', u'long'], priority = 3)

        tasks = self.gtd.getTasks(without_tags = u'1 minute')
        self.assertEqual(1, len(tasks))
        self.assertEqual(task3, tasks[0])

        tasks = self.gtd.getTasks(tags = u'work', without_tags = u'long')
        self.assertEqual(1, len(tasks))
        self.assertEqual(task2, tasks[0])

    def testModify(self):
        task1 = self.gtd.addTask(title = u'First',  tags = [u'home', u'1 minute'], priority = 1)
        task1.priority = 5
        task1.setTags([u'work', u'about hour'])

        task = self.gtd.getTaskById(task1.id)
        self.assertEqual(5, task.priority)
        self.assertEqual(2, len(task.tags))
        self.assertEqual(u'work',       task.tags[0].title)
        self.assertEqual(u'about hour', task.tags[1].title)

    def testCloseTask(self):
        task1 = self.gtd.addTask(title = u'First', priority = 10)
        task2 = self.gtd.addTask(title = u'Second', priority = 1)

        self.assertEqual(2, len(self.gtd.getTasks()))
        self.gtd.closeTask(task1.id)

        tasks = self.gtd.getTasks()
        self.assertEqual(1, len(tasks))
        self.assertEqual(u'Second', tasks[0].title)

        tasks = self.gtd.getTasks(show = 'all')
        self.assertEqual(2, len(tasks))
        self.assertEqual(u'First',  tasks[0].title)
        self.assertEqual(u'Second', tasks[1].title)

    def testCloseUnknown(self):
        self.assertRaises(TaskNotFound, self.gtd.closeTask, 12345)

    def testDeleteTask(self):
        task1 = self.gtd.addTask(title = u'First', priority = 10)

        self.assertEqual(1, len(self.gtd.getTasks(show = 'all')))
        self.gtd.deleteTask(task1.id)
        self.assertEqual(0, len(self.gtd.getTasks(show = 'all')))

    def testGetTasksNegation(self):
        task1 = self.gtd.addTask(title = u'First',  priority = 1)
        task2 = self.gtd.addTask(title = u'Second', priority = 2)

        tasks = self.gtd.getTasks()
        self.assertEqual(2, len(tasks))
        self.assertEqual(task2, tasks[0])
        self.assertEqual(task1, tasks[1])

    def testShowModes(self):
        self.gtd.closeTask(self.gtd.addTask(title = u'Closed', priority = 10).id)
        self.gtd.addTask(title = u'Open', priority = 1)

        # by default, only 'open' tasks
        tasks = self.gtd.getTasks()
        self.assertEqual(1, len(tasks))
        self.assertEqual(u'Open', tasks[0].title)

        tasks = self.gtd.getTasks(show = 'all')
        self.assertEqual(2, len(tasks))
        self.assertEqual(u'Closed', tasks[0].title)
        self.assertEqual(u'Open',   tasks[1].title)

        tasks = self.gtd.getTasks(show = 'closed')
        self.assertEqual(1, len(tasks))
        self.assertEqual(u'Closed', tasks[0].title)

        self.assertRaises(AssertionError, self.gtd.getTasks, show = 'bad-mode')

    def testDeleteTag(self):
        task = self.gtd.addTask(title = u'First', tags = [u'one', u'two', u'three'])

        self.gtd.deleteTag(u'two')
        tags = self.gtd.getTags()

        self.assertEqual(2, len(tags))
        self.assertEqual(2, len(self.gtd.getTaskById(task.id).tags))

        next_tag = tags[0]
        remaining_tag = tags[1]
        self.gtd.deleteTag(next_tag.id)

        tags = self.gtd.getTags()
        self.assertEqual(1, len(tags))
        self.assertEqual(1, len(self.gtd.getTaskById(task.id).tags))
        self.assertEqual(remaining_tag, tags[0])

