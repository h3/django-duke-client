from abc import abstractmethod

class BaseCommand(object):
    @abstractmethod
    def call(self):
        pass
    

def send_command(cmd, *args, **kwargs):
    class_name = '%sCommand' % (cmd[0].capitalize() + cmd[1:])
    module  = __import__('dukeclient.commands.%s' % cmd, {}, {}, class_name)
    command = getattr(module, class_name)()
    command.call(*args, **kwargs)

