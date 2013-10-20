# -*- coding: utf-8 -*-

import errno
import hmac
import logging
import os
import re
import shutil
import sys

from hashlib import sha1

import dukeclient

def color(string=None, c=None):
    """
    Returns a string wrapped in a shell color.
    If no color is given, the string is returned prefixed
    with the color reset code. if no arguments are provided at all,
    the color reset code is returned.
    """
    if c is None:
        if string is None:
            return "\x1b[0m"
        else:
            return "\x1b[0m%s" % string
    else:
        _c = {
            'black':'0;30',  'bold_black':'1;30',  'under_black':'4;30',
            'red':'0;31',    'bold_red':'1;31',    'under_red':'4;31',
            'green':'0;32',  'bold_green':'1;32',  'under_green':'4;32',
            'yellow':'0;33', 'bold_yellow':'1;33', 'under_yellow':'4;33',
            'blue':'0;34',   'bold_blue':'1;34',   'under_blue':'4;34',
            'purple':'0;35', 'bold_purple':'1;35', 'under_purple':'4;35',
            'cyan':'0;36',   'bold_cyan':'1;36',   'under_cyan':'4;36',
            'white':'0;37',  'bold_white':'1;37',  'under_white':'4;37',
        }
        return "\x1b[%sm%s\x1b[0m" % (_c[c.lower()], string)


def get_template_path(template):
    """
    Returns the custom template path if it exists.
    Else it returns the dukeclient/templates/ path.

    >>> get_template_path('env')
    ~/.duke/templates/env
    """
    path = os.path.join(os.getenv("HOME"), '.duke/templates/', template)
    if os.path.exists(path):
        return path
    else:
        return os.path.join(os.path.dirname(\
                dukeclient.__file__), 'templates/', template)

def copy_template(template, dest, src=False):
    """
    Copy a raw template to a specific destination (no context)

    >>> copy_template('env', '~/.duke/templates/')
    True
    """
    dest = os.path.join(dest, template)
    if src is False:
        src  = get_template_path(template)
    shutil.copy2(src, dest)


def create_from_template(template, dest, variables=None,dest_name=None):
    """
    Copy a template to a specific destination. The variables kwargs should
    either be False or a dictionary. If the later is provided, it will be
    used for variables substitution in the template.

    >>> create_from_template('env', '/project/path/.duke/',\
    >>> {'project': 'my_project'})
    True
    """
    dest_name = dest_name or template
    dest = os.path.join(dest, dest_name)
    src  = get_template_path(template)
    fs   = open(src, 'r')
    fd   = open(dest, 'w+')
    buff = fs.read()
    if variables:
        args = [variables is False and buff or buff % variables]
        fd.write(*args)
    else:
        fd.write(buff)
    fd.close()
    fs.close()
    return True


def mkdir(path):
    os.makedirs(path)


def file_to_string(f):
    """
    Returns file content as string
    """
    fd = open(f)
    buf = fd.readlines()
    fd.close()
    return ''.join(buf)


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


def patched_python_path(document_root, project_name, site_packages=True):
    cache_path = os.path.join(document_root, '.duke/cache/eggs/')
    eggs_path = os.path.join(document_root, '.duke/eggs/')
    sources_path = os.path.join(document_root, '.duke/src/')
    virtualenv_path = os.path.join(document_root, 'virtualenv/')
    python_path = [document_root, os.path.join(document_root, project_name)]
    old_sys_path = sys.path

    for l in os.listdir(sources_path):
        p = os.path.join(sources_path, l)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, 'setup.py')):
            python_path.append(p)

    for l in os.listdir(eggs_path):
        p = os.path.join(eggs_path, l)
        if os.path.isdir(p) and p.endswith('.egg'):
            python_path.append(p)

    for l in os.listdir(cache_path):
        p = os.path.join(cache_path, l)
        if os.path.isdir(p) and p.endswith('.egg'):
            python_path.append(p)

    if site_packages:
        for p in old_sys_path:
            python_path.append(p)

    return python_path

"""

# USING VIRTUALENV + BUILDOUT

if os.path.exists(VIRTUALENVPATH):
    # http://code.google.com/p/modwsgi/wiki/VirtualEnvironments
    # Remember original sys.path.
    prev_sys_path = list(sys.path)

    # Add site-packages directory.
    for version in ['2.7', '2.6', '2.5']:
        new_site_dir = os.path.join(VIRTUALENVPATH, 'lib/python%s/site-packages/' % version)
        if os.path.exists(new_site_dir):
            site.addsitedir(new_site_dir)
            break

    # Add project's paths
    if path not in sys.path:
        sys.path.append(path)
        sys.path.append(os.path.join(path, PROJECT_NAME))
        contrib = os.path.join(path, 'contrib/')
        if os.path.exists(contrib):
            sys.path.append(contrib)

    # Reorder sys.path so new directories at the front.
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path

"""
