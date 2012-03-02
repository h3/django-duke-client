# -*- coding: utf-8 -*-

import os
import sys
import logging
import hmac

from hashlib import sha1

import dukeclient


def create_from_template(template, dest, variables=None):
    if os.path.exists(os.path.join(os.environ['HOME'], '.duke/templates')) and template in ('env', 'profile'):
        basedir = os.path.join(os.environ['HOME'], '.duke/')
    else:
        basedir = os.path.dirname(dukeclient.__file__)


    if os.path.isdir(dest):
        dest = os.path.join(dest, template)
    src = os.path.join(basedir, 'templates/', template)
    fs = open(src, 'r')
    fd = open(dest, 'w+')
    buff = fs.read()
    if variables:
        fd.write(buff % variables)
    else:
        fd.write(buff)
    fd.close()
    fs.close()
    if os.path.exists(os.path.join(os.environ['HOME'], '.duke/templates')) and template == 'env':
        create_from_template('profile', os.path.join(variables['duke_path'], 'bin/profile'), variables)

"""
Taken/modified from Sentry
https://github.com/dcramer/sentry/blob/master/sentry/utils/__init__.py
"""

def get_signature(key, message, timestamp):
    return hmac.new(key, '%s %s' % (timestamp, message), sha1).hexdigest()

def get_auth_header(signature, timestamp, client):
    return 'Duke duke_signature=%s, duke_timestamp=%s, duke_client=%s' % (
        signature,
        timestamp,
        dukeclient.VERSION,
    )

def parse_auth_header(header):
    return dict(map(lambda x: x.strip().split('='), header.split(' ', 1)[1].split(',')))
