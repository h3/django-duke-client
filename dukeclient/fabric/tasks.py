import os, sys

from fabric.api import *
from fabric.contrib import files
from fabric.contrib import files, console, django
from fabric.utils import abort, warn

from dukeclient.fabric.utils import *

DEFAULT_RSYNC_EXCLUDE = (
    '.DS_Store',
    '.git',
    '.hg',
    '*.pyc',
    'Thumbs.db',
    '.svn',
    '.sass-cache',
    '~*',
)

# TODO: use decorators for events

@task
def media_diff(from_role=None):
    if from_role is None:
        ls = 'ls -ABFgRhl1 --ignore=.svn'
        diff_1 = '/tmp/%s.%s' % (env.site['project'], get_role(env))

        sudo('%s %s > %s' % (ls, get_conf(env, 'media-root'), diff_1))
        get(diff_1, '/tmp/')
        sudo('rm -f %s' % diff_1)
        
        # TODO: determine actual MEDIA_ROOT using settings
        media_root = '%s/media/' % env.site['project']
        diff_2 = '/tmp/%s' % env.site['project']

        local('%s %s > %s' % (ls, media_root, diff_2))
        local('vim -fdRmMn %s %s' % (diff_1, diff_2))
        local('rm -f %s %s' % diff_1, diff_2)


@task
#@event(env, 'on-sync-media')
def media_sync(*dest_roles):
    """
    Synchronize media folder accross stages

    $ fab -R demo media_sync
    sync demo -> local, prod

    $ fab -R demo media_sync:local
    sync demo -> local

    $ fab -R demo media_sync:prod
    sync demo -> prod

    $ fab -R prod media_sync:demo
    sync prod -> demo

    """
    dispatch_event(env, 'on-sync-media')

    src_role = get_role(env)

    # If no dest_roles are specified, all available roles are used
    # except the currently active role
    if len(dest_roles) == 0:
        dest_roles = [x for x in get_roles(env) if x != src_role]
        dest_roles.append('local')

    if console.confirm("Media sync %s -> %s" % (src_role, ", ".join(dest_roles)), default=False):

        tarfile = '%s.tar.gz' % env.site['project']
        tmpdir  = '/tmp'
        tmpdest = os.path.join(tmpdir, tarfile)

        media_root   = get_conf(env, 'media-root')
        media_parent = os.path.abspath(os.path.join(media_root, '../'))
        media_folder = os.path.basename(os.path.abspath(media_root))

        sudo('tar -czf %s -C %s %s' % (tmpdest, media_parent, media_folder))
    
        for dest_role in dest_roles:
            if dest_role == 'local':
                get(tmpdest, tmpdir)
                local('cd %s && tar -xvzf %s; cd -' % (tmpdir, tmpdest))
                local('rsync --omit-dir-times --exclude ".svn" --exclude ".sass-cache" -pthrvz %s %s' % (\
                        os.path.join(tmpdir, media_folder), os.path.join(os.getcwd(), env.site['project'])))
            else:
                "Sync media to %s (NOT IMPLEMENTED)" % dest_role

    else:
        puts("Nothing changed.")

       #if console.confirm('Delete out of sync files ? (WARNING: permanent !)', default=False):
       #    delete = True
       #else:
       #    delete = False

    dispatch_event(env, 'on-sync-media-done')


@task
def setup_permissions():
    """
    Setup directory permissions
    """
    dispatch_event(env, 'on-setup-permissions')
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
    
    dispatch_event(env, 'on-setup-permissions-done')


@task
def setup_virtualenv():
    """
    Setup virtualenv
    """
    dispatch_event(env, 'on-setup-virtualenv')
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
    dispatch_event(env, 'on-setup-virtualenv-done')

@task
def update_code(reload=True):
    """
    Update code on the servers.
    """
    project_path = get_project_path(env)

    with cd(project_path):
        if is_svn(env):
            sudo('svn up')
        elif is_git(env):
            sudo('git reset --hard')
            sudo('git pull')

@task
def checkout_code(reload=True):
    """
    Update code on the servers.
    """
    project_path = get_project_path(env)
    kind, repos = get_repos(env)
    if kind == 'svn':
        sudo('svn co %s %s' % (repos, project_path))
    elif kind == 'git':
        sudo('git clone %s %s' % (repos, project_path))


@task
def deploy_code(reload=True):
    """
    Checkout or update code on the servers.
    """
    puts("Deploying code to %s" % get_role(env))
    docroot = get_conf(env, 'document-root')
    project_path = get_project_path(env)

    if not files.exists(docroot):
        sudo('mkdir -p %s' % docroot)

    if not files.exists(project_path):
        checkout_code(reload=False)
    else:
        update_code(reload=False)
    if reload:
        apache('reload')


@task
def apache(cmd):
    """
    Manage the apache service. For example, `fab apache:restart`.
    """
    dispatch_event(env, 'on-apache-reload')
    if files.exists('/usr/sbin/invoke-rc.d'):
        sudo('invoke-rc.d apache2 %s' % cmd)
    elif files.exists('/etc/init.d/httpd'):
        if cmd == 'reload': cmd = 'graceful'
        sudo('/etc/init.d/httpd %s' % cmd)
    else:
        puts("WARNING: UNKNOWN HTTP SERVER TYPE OR CONFIGURATION, CANNOT RELOAD")
        sys.exit(1)
    dispatch_event(env, 'on-apache-reload-done')


@task
def buildout(reload=True):
    """
    Run buildout on the project
    """
    require_root_cwd()
    dispatch_event(env, 'on-buildout')
    duke_init(env)

    cfg = 'buildout.cfg'
    project_path = get_project_path(env)
    buildout_bin = os.path.join(project_path, '.duke/bin/buildout')
    custom_cfg = os.path.join(project_path, '%s.cfg' % get_role(env))

    if files.exists(custom_cfg):
        puts("Using custom config (%s)" % custom_cfg)
        cfg = custom_cfg
    else:
        puts("Using default config (%s)" % cfg)

    with cd(project_path):
        sudo('%s -vvv -c %s' % (buildout_bin, cfg))

    if reload:
        apache('reload')

    dispatch_event(env, 'on-buildout-done')


@task
def deploy(reload=True):
    """
    Quick deploy: new code and an in-place reload.
    """
    require_root_cwd()
    dispatch_event(env, 'on-deploy')
    deploy_code(reload=reload)
    setup_settings(reload=False)
    collectstatic()
    setup_permissions()
    dispatch_event(env, 'on-deploy-done')


@task
def full_deploy(no_input=False):
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
    require_root_cwd()
    dispatch_event(env, 'on-deploy')

    vhost_file = '%s.vhost' % env.name
    vhost = os.path.join(os.getcwd(), 'deploy/', vhost_file)
    if no_input or not os.path.exists(vhost) \
        and console.confirm("Warning vhost file not found: deploy/%s, abort ?" % vhost_file, default=True):
        dispatch_event(env, 'on-deploy-aborted')
        sys.exit(0)

    if get_conf(env, 'virtualenv'):
        setup_virtualenv()
    deploy_code(reload=False)
    buildout()
    setup_settings(reload=False)
   #if no_input or console.confirm("Run syncdb ?", default=False):
   #   syncdb()
    setup_vhost(reload=False)
    collectstatic()
    apache('reload')
    setup_permissions()
    dispatch_event(env, 'on-deploy-done')


@task
def setup_vhost(reload=True):
    """
    Setup virtual host
    """
    require_root_cwd()
    dispatch_event(env, 'on-setup-vhost')
    vhost = os.path.join(os.getcwd(), 'deploy/%s.vhost' % env.name)
    if os.path.exists(vhost):
        files.upload_template(vhost, get_conf(env, 'vhost-conf'), 
                context=get_context(env), use_sudo=True, backup=False)
        if reload:
            apache('reload')
    dispatch_event(env, 'on-setup-vhost-done')


@task
def setup_settings(reload=True):
    """
    Setup production settings
    """
    require_root_cwd()
    dispatch_event(env, 'on-setup-settings')
    settings_file = os.path.join(os.getcwd(), 'deploy/%s_settings.py' % env.name)
    if os.path.exists(settings_file):
        dest_path = os.path.join(get_conf(env, 'document-root'), env.site['package'], 
                        env.site['project'], 'local_settings.py')
        files.upload_template(settings_file, dest_path, 
                context=get_context(env), use_sudo=True, backup=False)
        if reload:
            apache('reload')
    dispatch_event(env, 'on-setup-settings-done')


@task
def collectstatic():
    """
    Run django collectstatic
    """
    require_root_cwd()
    dispatch_event(env, 'on-django-collectstatic')
    if get_conf(env, 'static-copy', False):
        django('collectstatic --noinput')
    else:
        django('collectstatic --noinput --link')
    dispatch_event(env, 'on-django-collectstatic-done')


@task
def syncdb():
    """
    Run django syncdb.
    """
    require_root_cwd()
    dispatch_event(env, 'on-django-syncdb')
    django('syncdb')
    dispatch_event(env, 'on-django-synchdb-done')
    #django('migrate')


@task
def django(cmd):
    """
    Helper: run a management command remotely.
    """
    require_root_cwd()
    django = os.path.join(get_project_path(env), '.duke/bin/django')
    cmd = '%s %s --settings=%s.settings' % (django, cmd, env.site['project'])
    dispatch_event(env, 'on-django-' + cmd)
    sudo(cmd)
    dispatch_event(env, 'on-django-' + cmd + '-done')


#@task
#def copy_db():
#    """
#    Copy the production DB locally for testing.
#    """
#    local('ssh %s pg_dump -U djangoproject -c djangoproject | psql djangoproject' % env.hosts[0])

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

