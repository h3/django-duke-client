import os, sys
import shutil
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils import create_from_template
#from dukeclient import client

class CleanCommand(BaseCommand):

    DIRS  = ['.duke']
    FILES = ['.mr.developer.cfg', 'bootstrap.py']
    BASE_PATH = os.getcwd()

    options = [
        ('-d', '--dev', {
            'dest': 'dev', 'action': 'store_true', 'default': False,
            'help': 'Recreate dev.cfg (data lost danger!)'}),
        ('-b', '--buildout', {
            'dest': 'buildout', 'action': 'store_true', 'default': False,
            'help': 'Recreate buildout.cfg (data lost danger!)'}),
        ('-s', '--src', {
            'dest': 'src', 'action': 'store_true', 'default': False,
            'help': 'Delete src/ (data lost danger!)'}),
        ('-S', '--setup', {
            'dest': 'setup', 'action': 'store_true', 'default': False,
            'help': 'Recreate setup.py (data lost danger!)'}),
    ]

    def call(self, *args, **options):

        if options['dev']:      self.FILES.append('dev.cfg')
        if options['buildout']: self.FILES.append('buildout.cfg')
        if options['src']:      self.DIRS.append('src')
        if options['setup']:    self.FILES.append('setup.py')

        for d in self.DIRS:
            path = os.path.join(self.BASE_PATH, '%s/' % d)
            if os.path.exists(path):
                shutil.rmtree(path)
                self.debug('deleted %s' % path)

        for f in self.FILES:
            path = os.path.join(self.BASE_PATH, f)
            if os.path.exists(path):
                os.remove(path)
                self.debug('deleted %s' % path)
    
        if 'DUKE_ENV' in os.environ:
            # TODO: check if it's possible to exit a loaded duke shell environment from here
            self.info("Cleaned. You must now exit this environment.")
