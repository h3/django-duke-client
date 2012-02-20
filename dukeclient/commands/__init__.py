import os, sys
import commands
from abc import abstractmethod

from dukeclient.utils import simplejson

class BaseCommand(object):

    def __init__(self, shell=False):
        self.is_shell = shell

    def option(self, name, value=None):
        if value:
            self._options[name] = value
            return value
        if self.is_shell:
            return self._options[name]
        else:
            if name in self._options:
                return self._options[name]
            else:
                return False

    @abstractmethod
    def call(self):
        pass

    def local(self, cmd):
        """
        Execute a given command locally
        """
        return commands.getstatusoutput(cmd)

    def json(self, string):
        return simplejson.loads(string)

    def exit(self, code=0):
        sys.exit(0)

    def debug(self, msg):
        print "Debug: %s" % msg

    def info(self, msg):
        print msg

    def warning(self, msg):
        print "Warning: %s" % msg

    def error(self, msg):
        print "Error: %s" % msg
        self.exit(1)


def get_command(cmd):
    class_name = '%sCommand' % (cmd[0].capitalize() + cmd[1:])
    module  = __import__('dukeclient.commands.%s' % cmd, {}, {}, class_name)
    return getattr(module, class_name)(shell=True)

def send_command(cmd, *args, **kwargs):
    return get_command(cmd).call(*args, **kwargs)

def get_command_options(cmd, *args, **kwargs):
    return getattr(get_command(cmd), 'options', [])
