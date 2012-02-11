import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils import create_from_template
#from dukeclient import client
# ./buildout -c .duke/buildout.cfg

class InitCommand(BaseCommand):

    options = [
        ('-d', '--distribute', {
            'dest': 'distribute', 'action': 'store_true', 'default': False,
            'help': 'Use distribute instead of setuptools'}),
        ('-p', '--python', {
            'dest': 'python', 
            'help': 'Python version to use (defaults to system default). Ex: python2.7'}),
    ]

    base_path = os.getcwd()

    def call(self, *args, **options):
        if len(args) < 2:
            self.info("usage: duke init <project> [options]\n")
            sys.exit(1)

        if args[1][:1] == '/':
            project_name = args[1].split('/')[-2]
        else:
            project_name = args[1].split('/')[-1]

        # bootstrap.py
        if os.path.exists(os.path.join(self.base_path, 'bootstrap.py')):
            self.warning("Found a bootstrap.py file.. skipping its creation.")
        else:
            self.info("Installing bootstrap.py..")
            create_from_template('bootstrap.py', self.base_path)

        # buildout.cfg
        print self.base_path
        if os.path.exists(os.path.join(self.base_path, 'buildout.cfg')):
            self.info("A buildout.cfg file has been found, will be using it.")
        else:
            self.info("Installing default buildout.cfg file")
            create_from_template('buildout.cfg', self.base_path, {
                'project_name': project_name,
                # TODO: find the parent dir automatically..
                'parent_dirname': 'duke-website'})

        self.info("Initializing zc.buildout")
        
        boot_opts = ''
        python = getattr(options, 'python', 'python')
        if getattr(options, 'distribute', False):
            opts = ' -d'
        status, output = self.local('%s bootstrap.py%s' % (python, boot_opts))
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

