import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.commands.dev import DevCommand
from dukeclient.utils import copy_template

class CustomizeCommand(BaseCommand):
    """
    Copy customization files to a specified location. (Defaults to ~/.duke)
    """

    options = [
        ('-t', '--target-directory', {
            'dest': 'target_directory', 'default': os.path.expanduser('~/.duke/'),
            'help': 'Copy profile and template files to a specified directory \
(default: ~/.duke/)'}),
    ]

    def call(self, *args, **options):
        self.target_directory = options['target_directory']
        self.templates_path   = os.path.join(self.duke_path, 'bin/')

        print __file__
        print args

#       if len(args) < 1:
#           self.error("usage: duke init <project> [options]\n")



#       if not os.path.exists(self.duke_path):
#           os.makedirs(self.duke_path)

#       # FIXME: Validate for proper python module name
#       project_name = args[0].replace('/', '').replace('-', '_')


#       # bootstrap.py
#       if os.path.exists(os.path.join(self.base_path, 'bootstrap.py')):
#           self.warning("Found a bootstrap.py file.. skipping its creation.")
#       else:
#           self.info("Installing bootstrap.py..")
#           create_from_template('bootstrap.py', self.base_path)

#       # Variables passed to generated .cfg files
#       context = {
#           'duke_client_version': dukeclient.VERSION,
#           'project_name': project_name,
#           'parent_dirname': os.path.basename(os.path.abspath(self.base_path)),
#           'base_path': self.base_path,
#           'duke_path': self.duke_path,
#           'settings_module': 'settings',
#       }

#       # buildout.cfg
#       if os.path.exists(os.path.join(self.base_path, 'buildout.cfg')):
#           self.info("A buildout.cfg has been found, will be using it.")
#       else:
#           self.info("Installing default buildout.cfg")
#           create_from_template('buildout.cfg', self.base_path, context)

#       # .duke/base.cfg
#       if os.path.exists(os.path.join(self.duke_path, 'base.cfg')):
#           self.info("A base.cfg has been found, will be using it.")
#       else:
#           self.info("Installing default base.cfg")
#           create_from_template('base.cfg', self.duke_path, context)

#       # .duke/dev.cfg
#       if os.path.exists(os.path.join(self.base_path, 'dev.cfg')):
#           self.info("A dev.cfg has been found, will be using it.")
#       else:
#           self.info("Installing default dev.cfg")
#           create_from_template('dev.cfg', self.base_path, context)

#       self.info("Initializing zc.buildout")
#       
#       boot_opts = ''
#       python = options['python'] or 'python' # and python !

#       # Even though distribute is considered superior and better maintained
#       # than setuptools, it is disabled by default because I cannot get the
#       # project sandboxing to work properly with it .. bummer.
#       if options['distribute']:
#           opts = ' -d'

#       status, output = self.local('%s bootstrap.py%s' % (python, boot_opts))
#       self.debug(output)

#       # Dev source
#       self.info("Installing dev hooks")

#       if not os.path.exists(self.bin_path):
#           os.makedirs(self.bin_path)

#       create_from_template('dev', self.bin_path, context)
#       print "creating the env file"
#       create_from_template('env', self.bin_path, context)
#       print "env file created"

#       self.info("Done!\n")
#       self.info("Type \"buildout\" to build the environment and install requirements.")

#       if not options['nodev']:
#           DevCommand().call()

