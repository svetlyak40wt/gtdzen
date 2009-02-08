import os
from models import *
from elixir import metadata, setup_all, create_all, session
from sqlalchemy.sql import not_
from utils import get_or_create
from pdb import set_trace

__version__ = '0.1.0'

class GTD(object):
    def __init__(self, filename):
        metadata.bind = 'sqlite:///%s' % filename
        metadata.bind.echo = True
        if not os.path.exists(filename):
            setup_all()
            create_all()

    def addTask(self, title, note = None, tags = [], priority = 1):
        task = Task(
            title = title,
            note = note,
            tags = self._createTags(tags),
            priority = priority)
        session.commit()
        return task

    def getTasks(self):
        return Task.query.all()

    def getTags(self):
        return Tag.query.all()

    def getTagsRelated(self, tags):
        if isinstance(tags, basestring):
            tags = [tags,]

#        set_trace()
        tasks_with_tags = [t[0] for t in session.query(Task.id).join(Tag).filter(Tag.title.in_(tags))]
        new_tags =  Tag.query.filter(Task.id.in_(tasks_with_tags)).filter(not_(Tag.title.in_(tags)))
        return new_tags

    def removeAll(self):
        for task in Task.query.all():
            task.delete()
        Tag.query.delete()
        session.commit()

    def _createTags(self, tags):
        return [get_or_create(Tag, title = tag) for tag in tags]

