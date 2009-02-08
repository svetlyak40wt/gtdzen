from elixir import Entity, Field, Unicode, UnicodeText, Integer, Float, ManyToMany

class Task(Entity):
    title = Field(Unicode(40))
    note = Field(UnicodeText)
    tags = ManyToMany('Tag')
    priority = Field(Float)

    def __str__(self):
        return '"%s" / %s (%s)>' % (self.title, self.priority, ', '.join(self.tags))

    def __repr__(self):
        return '<Task "%s" with tags %s>' % (self.title, ', '.join(self.tags))

class Tag(Entity):
    title = Field(Unicode(40), unique = True)
    tasks = ManyToMany('Task')

