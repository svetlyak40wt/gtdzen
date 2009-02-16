# This code is licensed under the New BSD License
# 2009, Alexander Artemenko <svetlyak.40wt@gmail.com>
# For other contacts, visit http://aartemenko.com

#!/usr/bin/env python
from migrate.versioning.shell import main
import os.path

#db_url = 'sqlite:///' + os.path.expanduser('~/todo.sqlite')
db_url = 'sqlite:///todo.sqlite'
main(url=db_url,repository='migrations')
