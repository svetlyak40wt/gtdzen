#!/usr/bin/env python -W ignore
import sys
import os
import gtdzen
from pdb import set_trace

def _parse_tags(tags):
    return [tag for tag in (tag.strip() for tag in tags.split(',')) if tag]

def _process_args(args):
    return [(arg != '-' and arg or None) for arg in (arg.decode('utf-8') for arg in args)]

class CommandUI:
    def __init__(self, database):
        self.gtd = gtdzen.GTD(database)

    def run(self, cmd_name, args):
        method = getattr(self, 'cmd_%s' % cmd_name, self.cmd_help)
        return method(*args)

    def cmd_add(self, title, priority = 1, tags = u''):
        task = self.gtd.addTask(
            title=title,
            priority=int(priority),
            tags = _parse_tags(tags),
        )
        print u'Task %s was added' % task

    def cmd_show(self, tags = u''):
        tasks = self.gtd.getTasks(_parse_tags(tags))
        if len(tasks) > 0:
            for task in tasks:
                print u'%d %s' % (task.id, task)
        else:
            print u'No tasks'

    def cmd_update(self, task_id, title = None, priority = None, tags = None):
        task = self.gtd.getTaskById(int(task_id))
        if title is not None:
            task.title = title
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.setTags(_parse_tags(tags))
        self.gtd.save(task)
        print u'Task %s was updated' % task

    def cmd_close(self, task_id):
        self.gtd.closeTask(int(task_id))
        print u'Task %s was closed' % task_id


    def cmd_help(self, *args):
        print u'GTDzen, version %s' % gtdzen.__version__
        print u'Usage: %s <command> [params...]' % sys.argv[0]


if __name__ == '__main__':
    cmd = len(sys.argv) > 1 and sys.argv[1] or ''
    args = len(sys.argv) > 1 and sys.argv[2:] or []

    ui = CommandUI(os.path.expanduser(u'~/todo.sqlite'))
    ui.run(cmd, _process_args(args))

