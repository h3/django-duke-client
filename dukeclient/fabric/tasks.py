import os, sys, datetime, glob

from fabric.api import *
from fabric.contrib import files
from fabric.contrib import files, console, django
from fabric.utils import abort, warn

from dukeclient.fabric.utils import *

django.settings_module('clientsbp.settings')
from django.conf import settings

if env.ssh_config_path and os.path.isfile(os.path.expanduser(env.ssh_config_path)):
    env.use_ssh_config = True


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
            branch = get_branch(env)
            if branch:
                sudo('git checkout %s' % branch)
            else:
                branch = 'master'
            sudo('git rebase %s' % branch)
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
        branch = get_branch(env)
        if branch:
            sudo('git checkout %s' % branch)


@task
def deploy_code(reload=True):
    """
    Checkout or update code on the servers.
    """
    puts("Deploying code to %s" % get_role(env))
    docroot = get_conf(env, 'document-root')
    project_path = get_project_path(env)

    if not files.exists(docroot, use_sudo=True):
        sudo('mkdir -p %s' % docroot)

    if not files.exists(project_path, use_sudo=True):
        checkout_code(reload=False)
    else:
        update_code(reload=False)
    if reload:
        reload_webserver()


@task
def reload_webserver(server=None):
    """
    Reloads the webserver. For example, `fab apache:nginx`.
    """
    reloaded = False
    error = False
    nginx_conf = os.path.join(os.getcwd(), 'deploy/%s.nginx' % env.name)
    if server == 'nginx' or os.path.exists(nginx_conf):
        dispatch_event(env, 'on-nginx-reload')
        sudo('service nginx reload')
        dispatch_event(env, 'on-nginx-reload-done')
        reloaded = True

    vhost_conf = os.path.join(os.getcwd(), 'deploy/%s.vhost' % env.name)
    if server == 'apache' or os.path.exists(vhost_conf):
        dispatch_event(env, 'on-apache-reload')
        if files.exists('/usr/bin/service'):
            sudo('service apache2 reload')
        elif files.exists('/usr/sbin/invoke-rc.d') and files.exists('/etc/init.d/apache2'):
            sudo('invoke-rc.d apache2 reload')
        elif files.exists('/etc/init.d/apache2'):
            sudo('/etc/init.d/apache2 reload')
        elif files.exists('/etc/init.d/httpd'):
            sudo('/etc/init.d/httpd graceful')
        else:
            error = True

        if error == False:
            reloaded = True
            dispatch_event(env, 'on-apache-reload-done')

    if not reloaded:
        puts("WARNING: UNKNOWN WEBSERVER TYPE OR CONFIGURATION, CANNOT RELOAD")
        dispatch_event(env, 'on-apache-reload-fail')


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
        reload_webserver()

    dispatch_event(env, 'on-buildout-done')


@task
def deploy(reload=True):
    """
    Quick deploy: new code and an in-place reload.
    """
    require_root_cwd()
    dispatch_event(env, 'on-deploy')
    deploy_code(reload=False)
    setup_settings(reload=False)
    setup_vhost(reload=False)
    setup_nginx(reload=False)
    setup_uwsgi(reload=reload)
    collectstatic()
    setup_permissions()
    if reload:
        reload_webserver()
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

    if get_conf(env, 'virtualenv'):
        setup_virtualenv()
    deploy_code(reload=False)
    buildout()
    setup_settings(reload=False)
   #if no_input or console.confirm("Run syncdb ?", default=False):
   #   syncdb()
    setup_vhost(reload=False)
    setup_nginx(reload=False)
    setup_uwsgi(reload=True)
    collectstatic()
    setup_permissions()
    reload_webserver()
    dispatch_event(env, 'on-deploy-done')


@task
def setup_uwsgi(reload=True):
    """
    Setup uwsgi
    """
    require_root_cwd()
    uwsgi_conf = os.path.join(os.getcwd(), 'deploy/%s.uwsgi' % env.name)
    if os.path.exists(uwsgi_conf):
        dispatch_event(env, 'on-setup-uwsgi')
        uwsgi_path = get_conf(env, 'uwsgi-conf')
        files.upload_template(uwsgi_conf, uwsgi_path,
                context=get_context(env), use_sudo=True, backup=False)
        if reload:
            sudo('touch %s' % uwsgi_path)
        dispatch_event(env, 'on-setup-uwsgi-done')


@task
def setup_vhost(reload=True):
    """
    Setup apache virtual host

     - deploy/$env.name.vhost

    """
    require_root_cwd()
    dispatch_event(env, 'on-setup-vhost')
    vhost_conf = os.path.join(os.getcwd(), 'deploy/%s.vhost' % env.name)
    if os.path.exists(vhost_conf):
        files.upload_template(vhost_conf, get_conf(env, 'vhost-conf'),
                context=get_context(env), use_sudo=True, backup=False)
        if reload:
            reload_webserver()
    dispatch_event(env, 'on-setup-vhost-done')


@task
def setup_nginx(reload=True):
    """
    Setup nginx site config

     - deploy/$env.name.nginx

    """
    require_root_cwd()
    nginx_conf = os.path.join(os.getcwd(), 'deploy/%s.nginx' % env.name)
    if os.path.exists(nginx_conf):
        dispatch_event(env, 'on-setup-nginx')
        nginx_path = get_conf(env, 'nginx-conf', '/etc/uwsgi/apps-enabled/%s.ini' % (u'%s.%s' % (env.name, env.site['domain'])))
        files.upload_template(nginx_conf, nginx_path,
                context=get_context(env), use_sudo=True, backup=False)
        if reload:
            reload_webserver()
    dispatch_event(env, 'on-setup-nginx-done')


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
            reload_webserver()
    dispatch_event(env, 'on-setup-settings-done')


@task
def collectstatic():
    """
    Run django collectstatic
    """
    require_root_cwd()
    dispatch_event(env, 'on-django-collectstatic')
    if get_conf(env, 'static-copy', False):
        django('collectstatic --noinput --verbosity=0')
    else:
        django('collectstatic --noinput --link --verbosity=0')
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


"""

EXPERIMENTAL

"""


@task
def media_diff(from_role=None):
    if from_role is None:
        ls = 'ls -ABFgRhl1 --ignore=.svn --ignore=*cache*'
        diff_1 = '/tmp/%s.%s' % (env.site['project'], get_role(env))

        sudo('%s %s > %s' % (ls, get_conf(env, 'media-root'), diff_1))
        get(diff_1, '/tmp/')
        sudo('rm -f %s' % diff_1)

        # TODO: determine actual MEDIA_ROOT using settings
        media_root = '%s/media/' % env.site['project']
        diff_2 = '/tmp/%s' % env.site['project']

        local('%s %s > %s' % (ls, media_root, diff_2))
        local('vim -fdRmMn %s %s' % (diff_1, diff_2))
        local('rm -f %s %s' % (diff_1, diff_2))


@task
def media_download(*dest_roles):
    src_role = get_role(env)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    tarfile = '%s-media-%s.tar.gz' % (env.site['project'], timestamp)
    tmpdest = os.path.join('/tmp', tarfile)
    media_root   = get_conf(env, 'media-root')
    media_parent = os.path.abspath(os.path.join(media_root, '../'))
    media_folder = os.path.basename(os.path.abspath(media_root))

    sudo('tar -czf %s -C %s %s --exclude-caches' % (tmpdest, media_parent, media_folder))
    get(tmpdest, os.getcwd())
    puts("Downloaded medias from %s" % src_role)


@task
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
def dumpdb(database='default', filename=None):
    role = get_role(env)
    if filename is None:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = u'dump-%s-%s-%s-%s.sql' % (env.site['project'], role, database, timestamp)

    tmpdest = os.path.join('/tmp', filename)

    run('mysqldump -u %s -p=%s %s > %s' % (
        settings.DATABASE_USER,
        settings.DATABASE_PASSWORD,
        settings.DATABASE_NAME,
        settings.DATABASE_HOST,
        filename
    ))
    get(tmpdest, os.getcwd())
    sudo('rm -f %s' % filename)
    puts('Database dumped to %s' % filename)

   #media_root   = get_conf(env, 'media-root')
   #media_parent = os.path.abspath(os.path.join(media_root, '../'))
   #media_folder = os.path.basename(os.path.abspath(media_root))

