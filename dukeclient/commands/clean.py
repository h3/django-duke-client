import os, sys
import shutil
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils import create_from_template
#from dukeclient import client

class CleanCommand(BaseCommand):

   #options = [
   #    ('-p', '--python', {'dest': 'python'}),
   #]

    base_path = os.getcwd()

    def call(self, *args, **options):
        dirs = ['parts', 'bin', 'eggs', 'develop-eggs']
        for d in dirs:
            path = os.path.join(self.base_path, '%s/' % d)
            if os.path.exists(path):
                shutil.rmtree(path)
                self.debug('deleted %s' % path)
