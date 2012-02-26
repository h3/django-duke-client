
==========
Cheatsheet
==========

.. contents::
   :depth: 3

Duke commands
=============

Note: An <argument> ending with -r means the command accepts Regular 
      Expressions

+----------------------------------------------------------------------------+
| `duke startproject <project-name>`  | Create a new project from scratch    |
+-------------------------------------+--------------------------------------+
| `duke init <project_name>`          | Initialize a django project\*        |
+-------------------------------------+--------------------------------------+
| `duke dev`                          | Start development environment        |
+-------------------------------------+--------------------------------------+

 \* Duke will create the project if it doesn't exists. It will also start the
    developent environment when done.

Dev commands
============

+-------------------------------------+--------------------------------------+
| `buildout`                          | Build or rebuild development env.    |
+-------------------------------------+--------------------------------------+
| `deactivate`                        | Exit development environment.        |
+-------------------------------------+--------------------------------------+
| `run_test`                          | Run .duke/bin/test                   |
+-------------------------------------+--------------------------------------+
| `dev`                               | Alias of develop                     |
+-------------------------------------+--------------------------------------+
| `dev activate <package-r>`          | Add packages to the list of          |
|                                     | development packages.                |
+-------------------------------------+--------------------------------------+
| `dev checkout <package-r>`          | Make a checkout of the packages      |
|                                     | matching the regular expressions and |
|                                     | add them to the list of development  |
|                                     | packages.                            |
+-------------------------------------+--------------------------------------+
| `dev deactivate <package-r>`        | Remove packages from the list of     |
|                                     | development packages.                |
+-------------------------------------+--------------------------------------+
| `dev info <package-r>`              | Lists informations about packages.   |
+-------------------------------------+--------------------------------------+
| `dev list <package-r>`              | Lists tracked packages.              |
+-------------------------------------+--------------------------------------+
| `dev purge <package-r>`             | Remove checked out packages which    |
|                                     | aren't active anymore.               |
+-------------------------------------+--------------------------------------+
| `dev rebuild/rb <package-r>`        | Run buildout with the last used      |
|                                     | arguments.                           |
+-------------------------------------+--------------------------------------+
| `dev reset <package-r>`             | Resets the packages develop status.  |
|                                     | This is useful when switching to a   |
|                                     | new buildout configuration.          |
+-------------------------------------+--------------------------------------+
| `dev status/stat/st <package-r>`    | Shows the status of tracked packages,| 
|                                     | filtered if <package-regexps> is     |
|                                     | given.                               |
+-------------------------------------+--------------------------------------+
| `dev update <package-r>`            | Updates all known packages currently |
|                                     | checked out.                         |
+-------------------------------------+--------------------------------------+
| `dev info <package-r>`              | Lists informations about packages.   |
+-------------------------------------+--------------------------------------+

Django commands & shortcuts
===========================

+-------------------------------------+--------------------------------------+
| `django`                            | Use this instead of manage.py        |
+-------------------------------------+--------------------------------------+
| `runserver`                         | Alias of `django runserver`          |
+-------------------------------------+--------------------------------------+
| `syncdb`                            | Alias of `django syncdb`             |
+-------------------------------------+--------------------------------------+
| `shell`                             | Alias of `django shell`              |
+-------------------------------------+--------------------------------------+
| `loaddata`                          | Alias of `django loaddata`           |
+-------------------------------------+--------------------------------------+
| `dumpdata`                          | Alias of `django dumpdata`           |
+-------------------------------------+--------------------------------------+

Git
===

+-------------------------------------+--------------------------------------+
| `gb`                                | Alias of `git branch`                |
+-------------------------------------+--------------------------------------+
| `gba`                               | Alias of `git branch -a`             |
+-------------------------------------+--------------------------------------+
| `gc`                                | Alias of `git commit -v`             |
+-------------------------------------+--------------------------------------+
| `gd`                                | Alias of `git diff`                  |
+-------------------------------------+--------------------------------------+
| `gl`                                | Alias of `git pull`                  |
+-------------------------------------+--------------------------------------+
| `gp`                                | Alias of `git push`                  |
+-------------------------------------+--------------------------------------+
| `gst`                               | Alias of `git status`                |
+-------------------------------------+--------------------------------------+
