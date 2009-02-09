from elixir import *
from sqlalchemy import *
from migrate import *
from pdb import *

metadata.bind = migrate_engine

class Task(Entity):
    title = Field(Unicode(40))
    note = Field(UnicodeText)
    tags = ManyToMany('Tag')
    priority = Field(Float)
    done = Field(Boolean, default = False)
    using_options(tablename='tasks', order_by='-priority')

class Tag(Entity):
    title = Field(Unicode(40), unique = True)
    tasks = ManyToMany('Task')
    using_options(tablename='tags', order_by='title')

try:
    setup_all()
except Exception:
    pass

def upgrade():
    for table in metadata.tables.values():
        table.create()

def downgrade():
    for table in metadata.tables.values():
        table.drop()
