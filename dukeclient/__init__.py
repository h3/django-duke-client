import urllib2
import base64
import time
import uuid
import logging

from dukeclient.utils import json, get_auth_header, get_signature
from dukeclient.utils.conf import ConfigManager

conf = ConfigManager()

VERSION = '0.0.1-alpha' 

REMOTE_TIMEOUT = 300
PROTOCOL = 'http' # https

#logger = logging.getLogger('dukeclient.errors')

class TempLogger(object):
    def log(self, *args, **kwargs):
        print args, kwargs
    def error(self, *args, **kwargs):
        print args, kwargs

logger = TempLogger()


class DukeClient(object):

    def _get_server_url(self, server):
        """
        Returns the server's URL constructed from the local config file
        """
        port = conf.get('port', server)
        out = [
            PROTOCOL,'://',
            conf.get('address', server),
            port and ':%s' % port or '',
            '/api/command/', 
        ]
        return "".join(out)

    def send_remote(self, url, data, headers={}):
        """
        Taken from Sentry
        """
        req = urllib2.Request(url, headers=headers)
        try:
            response = urllib2.urlopen(req, data, settings.REMOTE_TIMEOUT).read()
        except:
            response = urllib2.urlopen(req, data).read()
        return response

    def send(self, **kwargs):
        server = kwargs.get('server', 'default')
        if kwargs.get('data'):
            kwargs['data'] = kwargs['data'].copy()
        else:
            kwargs['data'] = {}

            kwargs['data'].update(dict(
                __dukeclient__= {'version': VERSION },
                message_id=uuid.uuid4().hex,
            ))
        message = base64.b64encode(json.dumps(kwargs).encode('zlib'))
        key = conf.get('key', server)
        timestamp = time.time()
        signature = get_signature(key, message, timestamp)
        headers = {
            'Authorization': get_auth_header(signature, timestamp, '%s/%s' % (self.__class__.__name__, VERSION)),
            'Content-Type': 'application/octet-stream',
        }

        try:
            #TODO: support for https
            address = "%sapi/command/" % self._get_server_url(server)
            rs = self.send_remote(url=address, data=message, headers=headers)
            return rs
        except urllib2.HTTPError, e:
            body = e.read()
            logger.error('Unable to reach Dukemaster server: %s (url: %%s, body: %%s)' % (e,), address, body,
                         exc_info=True, extra={'data': {'body': body, 'remote_url': address}})
            logger.log(kwargs.pop('level', None) or logging.ERROR, kwargs.pop('message', None))
        except urllib2.URLError, e:
            logger.error('Unable to reach Dukemaster server: %s (url: %%s)' % (e,), address,
                         exc_info=True, extra={'data': {'remote_url': address}})
            logger.log(kwargs.pop('level', None) or logging.ERROR, kwargs.pop('message', None))


client = DukeClient()
