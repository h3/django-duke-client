import os, sys
import dukeclient

from dukeclient.commands import BaseCommand

class DevCommand(BaseCommand):

   #options = [
   #    ('-p', '--python', {'dest': 'python'}),
   #]

    base_path = os.getcwd()

    def call(self, *args, **options):
        if not os.path.exists(os.path.join(self.base_path, '.duke/')):
            self.error("not within a duke managed project.")

        if os.getenv("DUKE_ENV"):
            env = os.path.basename(os.getenv("DUKE_ENV"))
            self.error("dev environment \"%s\" already loaded" % env)
        else:
            os.system('bash --rcfile .duke/bin/dev')
