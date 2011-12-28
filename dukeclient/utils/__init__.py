# -*- coding: utf-8 -*-

import os
import sys
import logging
import hmac

from hashlib import sha1

import dukeclient

def yes_no_prompt(message, default=False):

    if default:
        yn = "[Y/n]"
    else:
        yn = "[y/N]"

    rs = raw_input('%s %s: ' % (message, yn))

    if rs == '':
        return default

    elif rs not in ['y','yes','n', 'no']:
        return yes_no_prompt(message, default)

    else:
        return rs in ['y', 'yes']

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
