#!/usr/bin/env python -W ignore

# This code is licensed under the New BSD License
# 2009, Alexander Artemenko <svetlyak.40wt@gmail.com>
# For other contacts, visit http://aartemenko.com

import sys
import os
import locale
import shutil
import gtdzen
from ConfigParser import ConfigParser
from datetime import date
from pdb import set_trace

from gtdzen.exceptions import *

_language, _encoding = locale.getdefaultlocale()

def output(text):
    print text.encode(_encoding)

def _comma_split(string):
    return [s for s in (s.strip() for s in string.split(',')) if s]

_parse_tags = _comma_split

def _add_remove_tags(tags):
    """This method returns separates tags in two lists.
    First list contains only those tags with simple names
    or names with '+' prefix. Second list contains only
    tags with '-' prefix. Prefixes are stripped.

    >>> _add_remove_tags( [ '+a', 'a+', 'b', '-c', 'c-' ] )
    ([\'a\', \'a+\', \'b\', \'c-\'], [\'c\'])
    >>> _add_remove_tags( [] )
    ([], [])
    >>> _add_remove_tags( [ '' ] )
    Traceback (most recent call last):
    ...
    IndexError: string index out of range
    """
    return [t.lstrip('+') for t in tags if t[0] != '-'], \
           [t.lstrip('-') for t in tags if t[0] == '-']

def _parse_ids(ids):
    """
    >>> _parse_ids( '1, 2' )
    [1, 2]
    >>> _parse_ids( '1' )
    [1]
    """
    return map(int, _comma_split(ids))

def _process_args(args):
    """
    >>> _process_args( [ '-', 'bar', '-' ])
    [None, u'bar', None]
    """
    return [(arg != '-' and arg or None) for arg in (arg.decode('utf-8') for arg in args)]

class CommandUI:
    def __init__(self, database):
        self.gtd = gtdzen.GTD(database)

    def run(self, cmd_name, args):
        method = getattr(self, 'cmd_%s'%
                         cmd_name.replace('-', '_'), None)
        if method is None:
            raise Exception('Command "%s" not found.' % cmd_name)
        return method(*args)

    def cmd_add(self, title, priority = 1, tags = u''):
        "Add a new task with title, priority and tags."

        task = self.gtd.addTask(
            title=title,
            priority=int(priority),
            tags = _parse_tags(tags),
        )
        output(u'Task %s was added with id %d' % (task, task.id))

    def cmd_tags(self):
        "Show all tags with number of open/closed tasks."

        tags = self.gtd.getTags()
        if len(tags) > 0:
            for tag in tags:
                output(u'%d\t%s (%d/%d)' % (
                        tag.id, tag,
                        len(tag.open_tasks),
                        len(tag.closed_tasks)))
        else:
            output(u'No tags')

    def cmd_active_tags(self):
        "Show only tags with open tasks."

        tags = [t for t in self.gtd.getTags() if len(t.open_tasks) > 0]
        if len(tags) > 0:
            for tag in tags:
                output(u'%d\t%s (%d)' % (
                        tag.id, tag,
                        len(tag.open_tasks)))
        else:
            output(u'No tags')

    def cmd_del_tag(self, tag_ids):
        "Delete tag by id (comma-separated list can be passed to remove many tags)."

        for tag_id in _parse_ids(tag_ids):
            self.gtd.deleteTag(tag_id)
        output(u'These tags were deleted')

    def cmd_show(self, param = u'', mode = 'open'):
        "Show tasks by ids or filtered by tags."

        try:
            if not param:
                raise ValueError
            tasks = [self.gtd.getTaskById(task_id) for task_id in _parse_ids(param)]
        except ValueError:
            with_tags, without_tags = _add_remove_tags(_parse_tags(param))
            tasks = self.gtd.getTasks(
                        tags = with_tags,
                        without_tags = without_tags,
                        show = mode)

        if len(tasks) > 0:
            for task in tasks:
                output(u'%d %s' % (task.id, task))
        else:
            output(u'No tasks')

    def cmd_show_closed(self, *args, **kwargs):
        "Show closed tasks with given tags."
        return self.cmd_show(mode = 'closed', *args, **kwargs)

    def cmd_show_all(self, *args, **kwargs):
        "Show open and closed tasks with given tags."
        return self.cmd_show(mode = 'all', *args, **kwargs)

    def cmd_update(self, task_ids, title = None, priority = None, tags = None):
        "Update task or tasks and change title, priority or tags."

        if tags is not None:
            add_tags, remove_tags = _add_remove_tags(_parse_tags(tags))

        for task_id in _parse_ids(task_ids):
            task = self.gtd.getTaskById(task_id)

            if title is not None:
                task.title = title

            if priority is not None:
                task.priority = priority

            if tags is not None:
                new_tags = set(t.title for t in task.tags if t.title not in remove_tags)
                new_tags.update(add_tags)
                task.setTags(new_tags)

            self.gtd.save(task)
            output(u'Task %s was updated' % task)

    def cmd_close(self, task_ids):
        "Close task or tasks."

        for task_id in _parse_ids(task_ids):
            try:
                self.gtd.closeTask(task_id)
                output(u'Task %s was closed' % task_id)
            except TaskNotFound:
                output(u'Task %s not found' % task_id)

    def cmd_del_task(self, task_ids):
        "Close task or tasks."

        for task_id in _parse_ids(task_ids):
            task = self.gtd.getTaskById(task_id)
            if task is None:
                output('Task %d not found.' % task_id)
                continue

            yes_no = raw_input((u'Do you really want to delete task "%s"?\nAnswer "yes" or "no": ' % task.title).encode('utf-8'))
            if yes_no == 'yes':
                self.gtd.deleteTask(task_id)
                output(u'Task %s was deleted' % task_id)

    def cmd_test(self):
        "Doctests the program. Outputs nothing if all tests pass"

        import doctest
        doctest.testmod()

class Config(ConfigParser):
    def __init__(self, config_filename):
        ConfigParser.__init__(self)

        self.add_section('gtd')
        self.set('gtd', 'database', u'~/.gtd/todo.sqlite')
        self.set('gtd', 'backup', u'false')
        self.set('gtd', 'backup_dir', u'~/.gtd/backups')

        self.read(os.path.expanduser(config_filename))

def backup_database(path_to_db, path_to_backups):
    if os.path.exists(path_to_db):
        if not os.path.exists(path_to_backups):
            os.makedirs(path_to_backups)

        backup_file = os.path.join(path_to_backups, '%s.sqlite' % date.today())
        if not os.path.exists(backup_file):
            output(u'Writing backup to %s' % backup_file)
            shutil.copy2(path_to_db, backup_file)

def main():
    import logging
    from optparse import OptionParser
    from itertools import takewhile

    command_list = []
    command_help = {}

    for key in dir(CommandUI):
        if key.startswith( 'cmd' ):
            pname = key.split('_', 1)[-1]
            command_list.append(pname)
            command_help[pname] = getattr(CommandUI, key).__doc__

    usage="""%%prog <command> [params...]

Allowed commands:\n%s""" % '\n'.join(
    '  %s\n    : %s' % (cmd, command_help[cmd]) for cmd in command_list)

    parser = OptionParser( usage=usage,
                           version='GTDZen, version is %s.' % gtdzen.__version__ )

    parser.add_option( "-c", "--config", dest="config",
                       default=u'~/.gtdrc',
                       help="Turns on verbosity of the program" )
    parser.add_option( "-v", "--verbose", dest="verbose",
                       action="store_true", default=False,
                       help="Turns on verbosity of the program" )

    args_before_command = list(takewhile(lambda x: x not in command_list, sys.argv))
    (options, argv) = parser.parse_args(args_before_command)

    loglevel = logging.FATAL
    if options.verbose:
        loglevel = logging.DEBUG

    logging.basicConfig( level = loglevel,
                    format = '%(asctime)s %(levelname)s %(message)s' )
    log = logging.getLogger()

    log.debug( "argv=%s"%( argv ) )

    len_before = len(args_before_command)
    if len_before < len(sys.argv):
        cmd = sys.argv[len_before]
        args = sys.argv[len_before+1:]
    else:
        cmd = None
        args = []

    log.debug( "length of args=%s"%( len( args ) ) )
    log.debug( "cmd=%s"%( cmd ) )
    log.debug( "args=%s"%( args ) )

    if cmd not in command_list:
        parser.print_help()
        sys.exit(1)

    config = Config(options.config)
    database = os.path.expanduser(config.get('gtd', 'database'))

    if config.getboolean('gtd', 'backup'):
        backup_dir = os.path.expanduser(config.get('gtd', 'backup_dir'))
        backup_database(database, backup_dir)

    ui = CommandUI( database )
    ui.run(cmd, _process_args(args))

if __name__ == '__main__':
    main()
