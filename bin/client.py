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

from dukeclient.commands import send_command
from dukeclient.utils.conf import ConfigManager

conf = ConfigManager()


#def upgrade(interactive=True):
#    from dukemaster.conf import settings
#
#    call_command('syncdb', database=settings.DATABASE_USING or 'default', interactive=interactive)
#
#    if 'south' in django_settings.INSTALLED_APPS:
#        call_command('migrate', database=settings.DATABASE_USING or 'default', interactive=interactive)

def main():
    command_list = (
       #'deploy',           # ++++
       #'django',           # ++
       #'rollback',         # +
       #'service',          # +++
        'list',             # +++++
       #'importproject',    # +++++
       #'update',           # +++
       #'workon',           # ++++
       #'workout',          # +
    )
    args = sys.argv
    if len(args) < 2 or args[1] not in command_list:
        print "usage: duke [command] [options]"
        print
        print "Available subcommands:"
        for cmd in command_list:
            print " ", cmd
        sys.exit(1)

    parser = OptionParser(version="%%prog %s" % VERSION)

    cmd  = args[1]
    args = args[2:]

#   parser.add_option('--config', metavar='CONFIG')
    if cmd == 'list':
        parser.add_option('--master', metavar='SERVER')
#   if args[1] == 'start':
#       parser.add_option('--daemon', action='store_true', default=False, dest='daemonize')
#       parser.add_option('--no-daemon', action='store_false', default=False, dest='daemonize')
#       parser.add_option('--debug', action='store_true', default=False, dest='debug')

    (options, params) = parser.parse_args()

    if getattr(options, 'debug', False):
        django_settings.DEBUG = True

    send_command(cmd, *args)


#   elif args[0] == 'start':

#       if not os.path.exists(os.path.join(DUKEMASTER_ROOT, 'static/')):
#           from dukemaster.conf import settings
#           call_command('collectstatic', 
#                   database=settings.DATABASE_USING or 'default', 
#                   interactive=False)


    sys.exit(0)

if __name__ == '__main__':
    main()

