import os, sys

from fabric.api import *


def is_django(env):
    return files.exists(os.path.join(
            get_project_path(env), '.duke/bin/django'))


def get_role(env):
    """
    Returns the current active role
    """
    for role in env.roles:
        if env.host_string in env.roledefs[role]:
            return role


def get_roles(env):
    """
    Returns all available roles
    """
    return [x for x in env.roleconfs]



def get_conf(env, key, default=None):
    if not hasattr(env, 'conf'):
        env.name  = get_role(env)
        env.hosts = env.roleconfs[env.name]['hosts']
        env.conf  = env.roleconfs[env.name]

    try:
        v = env.conf[key]
    except:
        return default

    if isinstance(v, list):
        o = []
        for r in v:
            o.append(r % env.site)
        return o
    else:
        if isinstance(v, str):
            return v % env.site
        else:
            return v


def get_project_path(env):
    docroot = get_conf(env, 'document-root')
    return os.path.join(docroot, env.site['package'])


def dispatch_event(env, name):
    ctx = {
        'package': env.site['package'],
        'project': env.site['project'],
        'domain':  env.site['domain'],
    }
    ev = get_conf(env, name)
    if ev:
        for cmd in ev:
            sudo(cmd % ctx)


def duke_init(env):
    project_path = get_project_path(env)
    venv_root = os.path.join(get_conf(env, 'document-root'), 'virtualenv', env.site['project'])
    with cd(project_path):
        if get_conf(env, 'virtualenv'):
            pythonbin = os.path.join(venv_root, 'bin/python')
            sudo('duke init %s -n --python=%s' % (env.site['project'], pythonbin))
        else:
            sudo('duke init %s -n' % env.site['project'])


def require_root_cwd():
    if not os.path.exists(os.path.join(os.getcwd(), 'setup.py')):
        puts("You must be in the root directory of your project to use this command.")
        sys.exit(1)


def get_repos(env):
    if '+' in env.site['repos']:
        return env.site['repos'].split('+')
    else:
        if env.site['repos'].startswith('svn:'):
            return ('svn', env.site['repos'])
        elif env.site['repos'].startswith('svn:'):
            return ('git', env.site['repos'])


def get_branch(env):
    return get_conf(env, 'branch', env.site.get('branch', False))


def is_svn(env):
    return get_repos(env)[0] == 'svn'


def is_git(env):
    return get_repos(env)[0] == 'git'


def get_context(env, extra_context=None):
    ctx = {
        # Site global conf
        'domain': env.site['domain'],
        'package': env.site['package'],
        'project': env.site['project'],
        'repos': env.site['repos'],
        # Stage specific conf
        'hosts': get_conf(env, 'hosts'),
        'document-root': get_conf(env, 'document-root'),
        'media-root': get_conf(env, 'media-root'),
        'static-root': get_conf(env, 'static-root'),
        'vhost-conf': get_conf(env, 'vhost-conf'),
        'virtualenv': get_conf(env, 'virtualenv', False),
        'user': get_conf(env, 'user', 'www-data'),
        'group': get_conf(env, 'group', 'www-data'),
        'wsgi-processes': get_conf(env, 'wsgi-processes', 1),
        'wsgi-threads': get_conf(env, 'wsgi-threads', 5),
        'wsgi-user': get_conf(env, 'wsgi-user', get_conf(env, 'user', 'www-data')),
        'wsgi-group': get_conf(env, 'wsgi-group', get_conf(env, 'group', 'www-data')),
    }
    if extra_context is not None:
        ctx.update(extra_context)
    return ctx

