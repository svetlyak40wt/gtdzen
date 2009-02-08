#!/usr/bin/env python
import sys
import os
import gtdzen
from pdb import set_trace

def _parse_tags(tags):
    return [tag for tag in (tag.strip() for tag in tags.split(',')) if tag]

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
        for task in tasks:
            print u'%d %s' % (task.id, task)

    def cmd_help(self, *args):
        print u'GTDzen, version %s' % gtdzen.__version__
        print u'Usage: %s <command> [params...]' % sys.argv[0]


if __name__ == '__main__':
    cmd = len(sys.argv) > 1 and sys.argv[1] or ''
    args = len(sys.argv) > 1 and sys.argv[2:] or []

    ui = CommandUI(os.path.expanduser(u'~/todo.sqlite'))
    ui.run(cmd, [arg.decode('utf-8') for arg in args])

