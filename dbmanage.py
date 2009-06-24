#!/usr/bin/env python
# This code is licensed under the New BSD License
# 2009, Alexander Artemenko <svetlyak.40wt@gmail.com>
# For other contacts, visit http://aartemenko.com

from migrate.versioning.shell import main
import os.path
import gtdzen

#db_url = 'sqlite:///' + os.path.expanduser('~/todo.sqlite')
db_url = 'sqlite:///todo.sqlite'
main(url=db_url,repository=os.path.join(os.path.dirname(gtdzen.__file__), 'migrations'))
