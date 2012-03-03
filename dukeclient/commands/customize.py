import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.commands.dev import DevCommand
from dukeclient.utils import copy_template, mkdir

class CustomizeCommand(BaseCommand):
    """
    Copy customization files to a specified location. 
    Defaults to ~/.duke/templates/
    """

    options = [
        ('-t', '--target-directory', {
            'dest': 'target_directory', 'default': os.path.expanduser('~/.duke/templates/'),
            'help': 'Copy profile and template files to a specified directory \
(default: ~/.duke/)'}),
    ]

    def call(self, *args, **options):
        self.target_directory = options['target_directory']
        target = options['target_directory']
        tpl_path = os.path.join(os.path.dirname(dukeclient.__file__), 'templates/')

        mkdir(options['target_directory'])

        for template in os.listdir(tpl_path):
            # FIXME: the script should ask for overwirte if the
            # target file exists
            self.info("Copying %s to %s" % (template, target))
            copy_template(template, target, os.path.join(tpl_path, template))
