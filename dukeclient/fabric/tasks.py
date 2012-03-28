import os, sys

from fabric.api import *
from fabric.contrib import files
from dukeclient.fabric.utils import get_project_path, get_conf, get_role, event, duke_init


@task
def setup_permissions():
    """
    Setup directory permissions
    """
    user = get_conf(env, 'user')
    group = get_conf(env, 'group')
    docroot = get_conf(env, 'document-root')

    if user and group:
        sudo("chown -R %s:%s %s" % (user, group, docroot))
    elif user:
        sudo("chown -R %s %s" % (user, docroot))

    static_root = get_conf(env, 'static-root') 
    if static_root and files.exists(static_root):
        sudo("chmod -R 777 %s" % static_root)

    media_root = get_conf(env, 'media-root') 
    if media_root and files.exists(media_root):
        sudo("chmod -R 777 %s" % media_root)
    
    # FIXME: Dirty hack
    # The fabfile should run itself remotely to discover the database
    # type and path as described here:
    # http://docs.fabfile.org/en/1.4.0/api/contrib/django.html
    project_root = get_project_path(env)
    dev_db_root  = os.path.join(project_root, env.site['project'], 'dev.db')
    if files.exists(dev_db_root):
        sudo("chmod -R 777 %s" % dev_db_root)


@task
def setup_virtualenv():
    """
    Setup virtualenv
    """
    puts("Setuping virtualenv on %s" % env.host)
    venv_root = os.path.join(get_conf(env, 'document-root'), 'virtualenv')

    if not files.exists(venv_root):
        sudo('mkdir -p %s' % venv_root)

    with cd(venv_root):
        sudo("virtualenv --distribute --no-site-packages %s" % env.site['project'])

    user  = get_conf(env, 'user')
    group = get_conf(env, 'group')

    if user and group:
        sudo("chown -R %s:%s %s" % (user, group, venv_root))
    elif user:
        sudo("chown -R %s %s" % (user, venv_root))


@task
def deploy_code(reload=True):
    """
    Update code on the servers from SVN.
    """
    puts("Deploying code to %s" % get_role(env))
    docroot = get_conf(env, 'document-root')
    project_path = get_project_path(env)

    if not files.exists(docroot):
        sudo('mkdir %s' % docroot)

    if not files.exists(project_path):
        sudo('svn co %s %s' % (env.site['repos'], project_path))
    else:
        with cd(project_path):
            sudo('svn up')
    if reload:
        apache('reload')


@task
def apache(cmd):
    """
    Manage the apache service. For example, `fab apache:restart`.
    """
    event(env, 'on-reload')
    if files.exists('/usr/sbin/invoke-rc.d'):
        sudo('invoke-rc.d apache2 %s' % cmd)
    elif files.exists('/etc/init.d/httpd'):
        if cmd == 'reload': cmd = 'graceful'
        sudo('/etc/init.d/httpd %s' % cmd)
    else:
        print "WARNING: UNKNOWN HTTP SERVER TYPE OR CONFIGURATION, CANNOT RELOAD"
        sys.exit(1)
    event(env, 'on-reloaded')


@task
def buildout(reload=True):
    """
    Run buildout on the project
    """
   #_setup_duke()
    duke_init(env)
    project_path = get_project_path(env)

    with cd(project_path):
        sudo('%s -vvv -c buildout.cfg' % os.path.join(project_path, '.duke/bin/buildout'))

    if reload:
        apache('reload')


@task
def deploy(reload=True):
    """
    Quick deploy: new code and an in-place reload.
    """
    deploy_code(reload=reload)
    setup_permissions()


@task
def full_deploy():
    """
    Full deploy: 
    
     - setup virtualenv (?)
     - update code
     - run buildout
     - syncdb
     - update settings
     - setup vhost
     - collectstatic
     - reload apache

    """
    if get_conf(env, 'virtualenv'):
        setup_virtualenv()
    deploy_code(reload=False)
    buildout()
   #syncdb()
    setup_settings(reload=False)
    setup_vhost(reload=False)
    collectstatic()
    apache('reload')
    setup_permissions()
   #memcached("restart")


@task
def setup_vhost(reload=True):
    """
    Setup virtual host
    """
    vhost = os.path.join(LOCAL_PATH, 'deploy/%s.vhost' % env.name)
    if os.path.exists(vhost):
        files.upload_template(vhost, get_conf(env, 'vhost-conf'), context={
            'document-root': get_conf(env, 'document-root'),
            'package': env.site['package'],
            'project': env.site['project'],
            'domain': env.site['domain'],
        }, use_sudo=True, backup=False)
        if reload:
            apache('reload')


@task
def setup_settings(reload=True):
    """
    Setup production settings
    """
    settings_file = os.path.join(LOCAL_PATH, 'deploy/%s_settings.py' % env.name)
    if os.path.exists(settings_file):
        dest_path = os.path.join(get_conf(env, 'document-root'), env.site['package'], 
                        env.site['project'], 'local_settings.py')
        files.upload_template(settings_file, dest_path, context={
            'document-root': get_conf(env, 'document-root'),
            'package': env.site['package'],
            'project': env.site['project'],
            'domain': env.site['domain'],
        }, use_sudo=True, backup=False)
        if reload:
            apache('reload')


@task
def collectstatic():
    """
    Run django collectstatic
    """
    django('collectstatic --noinput --link')


@task
def syncdb():
    """
    Run django syncdb.
    """
    django('syncdb')
    #django('migrate')


@task
def django(cmd):
    """
    Helper: run a management command remotely.
    """
    django = os.path.join(get_project_path(env), '.duke/bin/django')
    sudo('%s %s --settings=%s.settings' % (django, cmd, env.site['project']))


@task
def copy_db():
    """
    Copy the production DB locally for testing.
    """
    local('ssh %s pg_dump -U djangoproject -c djangoproject | psql djangoproject' % env.hosts[0])

#@task
#def on(name):
#    """
#    Set the stage to work on, ex:
#
#    $ fab on:demo deploy
#
#    """
#    if not env.site.get(name, None):
#        raise Exception("Error: unknown stage %s" % name)
#    else:
#        env.hosts = env.site[name]['hosts']
#        env.conf  = env.site[name]
#        env.name  = name

#def southify(app):
#    """
#Southify an app remotely.
#
#This fakes the initial migration and then migrates forward. Use it the first
#time you do a deploy on app that's been newly southified.
#"""
#    managepy('migrate %s 0001 --fake' % app)
#    managepy('migrate %s' % app)

#def copy_docs():
#    """
#Copy build docs locally for testing.
#"""
#    local('rsync -av --delete --exclude=.svn %s:%s/ /tmp/djangodocs/' %
#            (env.hosts[0], env.deploy_base.child('docbuilds')))


#def update_docs():
#    """
#Force an update of the docs on the server.
#"""
#    managepy('update_docs', site='docs')


#def memcached(cmd):
#    """
#Manage the memcached service. For example, `fab memcached:--h`.
#"""
#    sudo('invoke-rc.d memcached %s' % cmd)


#def get_kernel_name():
#    run('uname -s')

