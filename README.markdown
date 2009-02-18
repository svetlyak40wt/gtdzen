GTDzen
======

This is a simple but flexible library and application to realize [Getting Things Done][gtd] method by David Allen.

GTDzen is based on a simplicity, so you'll not find any projects, contexts or areas of responsibility. I'm sure,
that all you need is smart tagging and correct priorities, I call it - "Tagged GTD Workflow".

Installation
------------

First of all, you need to install all requirements. Next, you can install gtdzen.

If you install from the source, run `python setup.py install`.

If you wish to install from the PyPi, use `easy_install gtdzen` or `pip install gtdzen`.

Tutorial
--------

There is only command line interface right now. But I'll be happy if somebody helps me to build a GUI for Mac OS X.

I use such aliases in the ZSH/BASH:

    alias gtshow='gtd show'
    alias gtwork='gtd show today,work'
    alias gthome='gtd show today,home'
    alias gtlate='gtd show -today'
    alias gta='gtd add'
    alias gtdone='gtd close'
    alias gtu='gtd update'

(This package includes 'aliases' file. You can "source" it in your shell's config.)

Using these aliases, you can quickly update and process your task list. For example:

Lets fill our task list:

    # gta "To write setup.py script" 10 today,project,python
    # gta "Add a new field to the model and update database schema." 8 today,project,python
    # gta "Find how to use sqlachemy-migration and sqlite" 5 project,python

Now you can list tasks for today:

    # gtshow today
    1 "To write setup.py script" / 10.0 (project, python, today)
    2 "Add a new field to the model and update database schema." / 8.0 (project, python, today)

Here, you can see two opened tasks for today, sorted by priority. Lets close first task:

    # gtdone 1
    Task 1 was closed
    # gtshow today
    2 "Add a new field to the model and update database schema." / 8.0 (project, python, today)

If you need more tasks, than you can look at tasks not planned for today, and update tags accordingly
to your workflow:

    # gtshow -today
    3 "Find how to use sqlachemy-migration and sqlite" / 5.0 (project, python)
    # gtu 3 - - -project,read,today,internet
    Task "Find how to use sqlachemy-migration and sqlite" / 5.0 (internet, python, read, today) was updated

The command 'gtd update' accepts almost the same parameters as 'gtd add' command, with few exceptions:

1 At first place, you must pass task or tasks numbers. If you update many task, than it must be a comma separated
  list, like this one: 1,5,3
2 If you don't want to change title, priority or tags, just pass minus symbol instead of them.
3 With 'update' command for add or remove tags. To add a new tag, just pass it's name as usual. To remove,
  add a prefix -.

Ok, it's all. Have a fun and build your own tagged GTD workflow.

TODO
----

* automatic database migrations.
* config file with basic options (where to store database, for example).
* bash/zsh autocomplete.
* task annotations.
* import/export to/from some XML format.

License
-------

This code is licensed under the New BSD License. See more details in the LICENSE file.

Contacts
--------

My name is Alexander Artemenko. Feel free to contact me by email or jabber: svetlyak.40wt@gmail.com.

Also, you can clone [this project at GitHub][at-github] and send me patches.


[gtd]: http://en.wikipedia.org/wiki/GTD
[at-github]: http://github.com/svetlyak40wt/gtdzen/
