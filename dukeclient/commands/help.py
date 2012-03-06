import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils import color as c


class HelpCommand(BaseCommand):
    """
    Show duke help.
    """

    options = []

    def call(self, *args, **options):
        self.base_path = 'base_path' in options and options['base_path'] or os.getcwd()
        self.duke_path = os.path.join(self.base_path, '.duke/')
        self.bin_path  = os.path.join(self.duke_path, 'bin/')
        self.conf_path = os.path.join(os.getenv("HOME"), '.duke/')

        print "[%s]" % c("Available environment commands", "bold_green")
        print "".join(['  %s\n' % x for x in os.listdir(self.bin_path)])
        
        # TODO: generate this list programmatically by 
        # grepping project/.duke/bin/env&profile
        # Note: only use python (nothing OS specific)
        print "[%s]" % c("Available environment shortcuts", "bold_green")
        shortcuts = ['buildout', 'dbshell', 'dev', 'dumpdata', 'loaddata',\
                     'python', 'runserver', 'shell', 'syncdb']
        print "".join(['  %s\n' % x for x in shortcuts])
