# -*- coding: utf-8 -*-

import hmac
import logging
import os
import shutil
import sys

from hashlib import sha1

import dukeclient

def get_template_path(template):
    """
    Returns the custom template path if it exists.
    Else it returns the dukeclient/templates/ path.

    >>> get_template_path('env')
    ~/.duke/templates/env
    """
    path = os.path.join(os.environ['HOME'], '.duke/templates/', template)
    if os.path.exists(path):
        return path
    else:
        return os.path.join(os.path.dirname(\
                dukeclient.__file__), 'templates/', template)

def copy_template(template, dest):
    """
    Copy a raw template to a specific destination (no context)

    >>> copy_template('env', '~/.duke/templates/')
    True
    """
    dest = os.path.join(dest, template)
    src  = get_template_path(template)
    shutil.copy2(src, dest)


def create_from_template(template, dest, variables=None):
    """
    Copy a template to a specific destination. The variables kwargs should 
    either be False or a dictionary. If the later is provided, it will be 
    used for variables substitution in the template.

    >>> create_from_template('env', '/proect/path/.duke/',\
    >>> {'project': 'my_project'})
    True
    """
    dest = os.path.join(dest, template)
    src  = get_template_path(template)
    fs   = open(src, 'r')
    fd   = open(dest, 'w+')
    buff = fs.read()
    print variables
    args = [variables is None and buff or buff % variables]
    fd.write(*args)
    fd.close()
    fs.close()
    return True

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
