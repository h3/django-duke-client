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
    env.name  = get_role(env)
    env.hosts = env.roleconfs[env.name]['hosts']
    env.conf  = env.roleconfs[env.name]

    context = {'env_name': env.name}
    context.update(env.conf)
    context.update(env.site)

    try:
        v = context[key]
    except KeyError:
        v = default


    if isinstance(v, list):
        o = []
        for r in v:
            o.append(r % context)
        return o
    elif isinstance(v, str):
        return v % context
    else:
        return v


def get_project_path(env):
    docroot = get_conf(env, 'document-root')
    return os.path.join(docroot, env.site['package'])


def dispatch_event(env, name):
    cmd_list = get_conf(env, name)
    if cmd_list:
        ctx = get_context(env)
        for cmd in cmd_list:
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
    slug = u'%s.%s' % (env.name, env.site['domain'])
    ctx = {
        # Global conf
        'domain': env.site['domain'],
        'package': env.site['package'],
        'project': env.site['project'],
        'repos': env.site['repos'],
        'user': get_conf(env, 'user', 'www-data'),
        'group': get_conf(env, 'group', 'www-data'),
        'hosts': get_conf(env, 'hosts'),
        'document-root': get_conf(env, 'document-root'),
        # Apache specific
        'vhost-conf': get_conf(env, 'vhost-conf'),
        'virtualenv': get_conf(env, 'virtualenv', False),
        'virtualenv-root': get_conf(env, 'virtualenv-root'),
        # Django specific
        'media-root': get_conf(env, 'media-root'),
        'static-root': get_conf(env, 'static-root'),
        # Apache+wsgi
        'wsgi-processes': get_conf(env, 'wsgi-processes', 1),
        'wsgi-threads': get_conf(env, 'wsgi-threads', 5),
        'wsgi-user': get_conf(env, 'wsgi-user', get_conf(env, 'user', 'www-data')),
        'wsgi-group': get_conf(env, 'wsgi-group', get_conf(env, 'group', 'www-data')),
        # Uwsgi
        'uwsgi-conf': get_conf(env, 'uwsgi-conf', '/etc/uwsgi/apps-enabled/%s.ini' % slug),
        'uwsgi-file': get_conf(env, 'uwsgi-file', os.path.join(get_conf(env, 'document-root'), get_conf(env, 'package'), get_conf(env, 'project'), 'app.wsgi')),
        'uwsgi-pass': get_conf(env, 'uwsgi-pass', '127.0.0.1:3030'),
        'uwsgi-master': get_conf(env, 'uwsgi-master', 'true'),
        'uwsgi-processes': get_conf(env, 'uwsgi-processes', 4),
        'uwsgi-fastrouter-cheap': get_conf(env, 'uwsgi-fastrouter-cheap', 'true'),
        'uwsgi-fastrouter-subscription-server': get_conf(env, 'uwsgi-fastrouter-subscription-server', '127.0.0.1:4040'),
        'uwsgi-req-logger': get_conf(env, 'uwsgi-req-logger', 'file:/var/log/uwsgi/app/%s-access' % slug),
        'uwsgi-logger': get_conf(env, 'uwsgi-logger', 'file:/var/log/uwsgi/app/%s-error' % slug),
        # nginx
        'nginx-conf': get_conf(env, 'nginx-conf', '/etc/nginx/site-enabled/%s' % slug),
        'nginx-listen': get_conf(env, 'nginx-listen', '0.0.0.0:80'),
        'nginx-server-name': get_conf(env, 'nginx-server-name', get_conf(env, 'domain')),
        'nginx-client-max-body-size': get_conf(env, 'nginx-client-max-body-size', '10M'),
    }
    if extra_context is not None:
        ctx.update(extra_context)
    return ctx

