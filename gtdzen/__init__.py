# This code is licensed under the New BSD License
# 2009, Alexander Artemenko <svetlyak.40wt@gmail.com>
# For other contacts, visit http://aartemenko.com

import os
import sys

try:
    from elixir import metadata, setup_all, create_all, session
    from models import *
    from sqlalchemy.sql import not_
except ImportError:
    """Ignore this imports because they may fail
       during __version__ import."""

from utils import get_or_create, make_list
from pdb import set_trace

from exceptions import *

__version__ = '0.1.3'
__all__ = ['GTD']

class GTD(object):
    def __init__(self, filename):
        db_url = 'sqlite:///' + filename
        metadata.bind = db_url
        #metadata.bind.echo = True
        setup_all()
        if not os.path.exists(filename):
            create_all()

    def addTask(self, title, note = None, tags = [], priority = 1):
        task = Task(
            title = title,
            note = note,
            tags = self._createTags(tags),
            priority = priority)
        session.commit()
        return task

    def getTaskById(self, task_id):
        return Task.query.get(task_id)

    def getTasks(self, tags = [], without_tags = [], show = 'open'):
        assert(show in ('all', 'open', 'closed'))
        query = Task.query

        tags = make_list(tags)
        for tag in tags:
            query = query.filter(Task.tags.any(title = tag))

        without_tags = make_list(without_tags)
        for tag in without_tags:
            query = query.filter(not_(Task.tags.any(title = tag)))

        if show != 'all':
            query = query.filter_by(done = (show == 'closed'))

        return query.all()

    def getTags(self):
        return Tag.query.all()

    def deleteTag(self, tag):
        """Delete tag by id or name"""
        if isinstance(tag, basestring):
            tag = Tag.query.filter_by(title = tag).one()
        else:
            tag = Tag.query.filter_by(id = tag).one()
        tag.delete()
        session.commit()

    def getTagsRelated(self, tags):
        tags = make_list(tags)

        tasks = session.query(Task.id).filter(
                    Task.tags.any(Tag.title.in_(tags)))
        task_ids = [t[0] for t in tasks]
        new_tags =  Tag.query.filter(Tag.tasks.any(Task.id.in_(task_ids))) \
                             .filter(not_(Tag.title.in_(tags)))
        return new_tags.all()

    def removeAll(self):
        for task in Task.query.all():
            task.delete()
        Tag.query.delete()
        session.commit()

    def save(self, obj):
        '''Updates object and commit session.'''
        obj.update()
        session.commit()

    def closeTask(self, task_id):
        task = self.getTaskById(task_id)
        if task is None:
            raise TaskNotFound

        task.done = True
        self.save(task)

    def deleteTask(self, task_id):
        task = self.getTaskById(task_id)
        session.delete(task)
        session.commit()

    def _createTags(self, tags):
        return [get_or_create(Tag, title = tag) for tag in tags]

