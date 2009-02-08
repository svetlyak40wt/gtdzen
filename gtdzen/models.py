from elixir import Entity, Field, Unicode, UnicodeText, Integer, Float, ManyToMany, using_options

class Task(Entity):
    title = Field(Unicode(40))
    note = Field(UnicodeText)
    tags = ManyToMany('Tag')
    priority = Field(Float)

    using_options(tablename='tasks', order_by='-priority')

    def __str__(self):
        return u'"%s" / %s (%s)' % (self.title, self.priority, ', '.join(map(unicode, self.tags)))

    def __repr__(self):
        return u'<Task "%s" with tags %s>' % (self.title, ', '.join(map(unicode, self.tags)))

class Tag(Entity):
    title = Field(Unicode(40), unique = True)
    tasks = ManyToMany('Task')

    using_options(tablename='tags', order_by='title')

    def __str__(self):
        return self.title

    def __repr__(self):
        return u'<Tag "%s">' % self.title

