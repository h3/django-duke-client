import os

from fabric.api import sudo, task


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
        return None

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
