# This code is licensed under the New BSD License
# 2009, Alexander Artemenko <svetlyak.40wt@gmail.com>
# For other contacts, visit http://aartemenko.com

from elixir import *
from utils import get_or_create
from pdb import set_trace

class Task(Entity):
    title = Field(Unicode(40), required = True)
    note = Field(UnicodeText)
    tags = ManyToMany('Tag')
    priority = Field(Float, default = 1, required = True)
    done = Field(Boolean, default = False, required = True)

    using_options(tablename='tasks', order_by='-priority')

    def __unicode__(self):
        return u'"%s" / %s %s (%s)' % (
            self.title, self.priority, self.done and 'CLOSED' or 'OPEN', ', '.join(map(unicode, self.tags)))

    def __repr__(self):
        return u'<Task "%s" with tags %s>' % (self.title, ', '.join(map(unicode, self.tags)))

    def setTags(self, tags):
        self.tags = [get_or_create(Tag, title = tag) for tag in tags]

class Tag(Entity):
    title = Field(Unicode(40), required = True, unique = True)
    tasks = ManyToMany('Task')

    using_options(tablename='tags', order_by='title')

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return u'<Tag "%s">' % self.title

    @property
    def open_tasks(self):
        return [t for t in self.tasks if not t.done]

    @property
    def closed_tasks(self):
        return [t for t in self.tasks if t.done]

