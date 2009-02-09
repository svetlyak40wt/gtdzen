#!/usr/bin/env python
from migrate.versioning.shell import main
import os.path

#db_url = 'sqlite:///' + os.path.expanduser('~/todo.sqlite')
db_url = 'sqlite:///todo.sqlite'
main(url=db_url,repository='migrations')
