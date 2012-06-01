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

    def call(self, *args, **options):
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

    # TODO: check if it's possible to exit a loaded duke shell environment from here
