import sys
import git

from dukeclient import client
from dukeclient.commands import BaseCommand

class CheckoutCommand(BaseCommand):
    """
    Checkout a project
    """

    accept_kwargs = ['servers', 'projects']

    def call(self, *a, **k):
        rs = self.json(client.send(command='checkout', args=a, flags=k))
        if rs['protocol'] == 'git':
            try:
                print git.Git().clone(rs['url'])
            except git.exc.GitCommandError, e:
                print "Error: %s" % e
            finally:
                sys.exit(0)


