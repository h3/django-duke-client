#!/usr/bin/env python

#from __future__ import with_statement
import imp
import logging
import os
import os.path
import sys

#from django.conf import settings as django_settings
#from django.core.management import call_command
from optparse import OptionParser

from dukeclient import VERSION

from dukeclient.commands import send_command, get_command_options
from dukeclient.utils.conf import ConfigManager

conf = ConfigManager()


# call_command('syncdb', database=settings.DATABASE_USING or 'default', interactive=interactive)
#
# if 'south' in django_settings.INSTALLED_APPS:
#     call_command('migrate', database=settings.DATABASE_USING or 'default', interactive=interactive)

def main():
    command_list = (
        'clean',
        'dev',
        'init',
        'startproject',
       #'deploy',           # ++++
       #'django',           # ++ ?
       #'rollback',         # +
       #'service',          # +++
       #'list',
       #'update',           # +++
    )

    if len(sys.argv) < 2 or sys.argv[1] not in command_list:
        print "usage: duke [command] [options]\n"
        print "Available subcommands:"
        for cmd in command_list:
            print " ", cmd
        sys.exit(1)

    parser = OptionParser(version="%%prog %s" % VERSION)
    cmd  = sys.argv[1]

#   parser.add_option('--config', metavar='CONFIG')
#   parser.add_option('--debug', action='store_true', default=False, dest='debug')

    
#   if cmd in ['list', 'checkout']:
#       parser.add_option('--master', metavar='SERVER')
    for opts in get_command_options(cmd):
        if isinstance(opts[1], dict): # ex: -h
           parser.add_option(opts[0], **opts[1])
        else: # ex: -h, --help
           parser.add_option(opts[0], opts[1], **opts[2])


    (options, args) = parser.parse_args()

    if getattr(options, 'debug', False):
        django_settings.DEBUG = True

    send_command(cmd, *args, **options.__dict__)

    sys.exit(0)

if __name__ == '__main__': # pragma: no cover
    main()
