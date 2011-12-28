from abc import abstractmethod
from dukeclient.utils import simplejson

class BaseCommand(object):

    @abstractmethod
    def call(self):
        pass

    def json(self, string):
        return simplejson.loads(string)
    

def send_command(cmd, *args, **kwargs):
    class_name = '%sCommand' % (cmd[0].capitalize() + cmd[1:])
    module  = __import__('dukeclient.commands.%s' % cmd, {}, {}, class_name)
    command = getattr(module, class_name)()
    return command.call(*args, **kwargs)

