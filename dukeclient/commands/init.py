import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils import create_from_template
#from dukeclient import client
# ./buildout -c .duke/buildout.cfg

class InitCommand(BaseCommand):

    options = [
        ('-p', '--python', {'dest': 'python'}),
    ]

    base_path = os.getcwd()

    def call(self, *args, **options):
        if len(args) < 2:
            self.info("usage: duke init <project> [options]\n")
            sys.exit(1)

        project_name = args[1].replace('/', '')

        # bootstrap.py
        if os.path.exists(os.path.join(self.base_path, 'bootstrap.py')):
            self.error("Project already initialized")
        else:
            self.info("Installing bootstrap.py..")
            create_from_template('bootstrap.py', self.base_path)

        # buildout.cfg
        if os.path.exists(os.path.join(self.base_path, 'buildout.cfg')):
            self.info("A buildout.cfg file has been found, will be using it.")
        else:
            self.info("Installing default buildout.cfg file")
            create_from_template('buildout.cfg', self.base_path, {
                'project_name': project_name})

        self.info("Initializing zc.buildout")
        
        python = getattr(options, 'python', 'python')
        status, output = self.local('%s bootstrap.py -d' % python)
        self.debug(output)

        # Dev source
        self.info("Installing dev hooks")
        dev_args = {
            'project_name': project_name,
            'base_path': self.base_path}

        create_from_template('dev', os.path.join(self.base_path, 'bin/'), dev_args)
        create_from_template('env', os.path.join(self.base_path, 'bin/'), dev_args)

        self.info("Done. It is recommanded to add bootstrap.py and buildout.cfg to your VCS.")
        
        #print client.send(command='list', args=a, flags=k)

