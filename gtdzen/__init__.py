import os
from models import *
from elixir import metadata, setup_all, create_all, session

__version__ = '0.1.0'

class GTD(object):
    def __init__(self, filename):
        metadata.bind = 'sqlite:///%s' % filename
        #metadata.bind.echo = True
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

    def removeAll(self):
        for task in Task.query.all():
            task.delete()
        Tag.query.delete()
        session.commit()

    def _createTags(self, tags):
        return [Tag(title = tag) for tag in tags]

