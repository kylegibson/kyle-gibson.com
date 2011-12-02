import pipes
from textwrap import dedent as _d

from fabric.api import *

from fabric.contrib.files import append,contains

#local_run = local
#remote_run = run

env.domain        = 'kyle-gibson.com'
env.local         = False
env.pythonversion = '2.7.2'
env.nginx_url     = 'http://nginx.org/download/nginx-1.0.10.tar.gz'
env.repo          = 'git://github.com/kylegibson/%(domain)s.git' % env
env.user          = 'frozen'
env.hosts         = ['frozen.frozenonline.com']
env.venv          = env.domain
env.pip_requirements = "pipfile"
env.path          = '$HOME/uwsgi/apps/%(domain)s' % env
env.log_path      = "%(path)s/logs" % env
env.access_log    = "%(log_path)s/access.log" % env
env.error_log     = "%(log_path)s/access.log" %env
env.static_url    = "/static";
env.static_path   = "%(path)s/staticroot" % env

@task
def foo():
    pass
    #print contains("~/.bash_profile", "pythonbrew", exact=False)
            #"[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc")

#def run(*args, **kwargs):
#    return (local_run if env.local else remote_run)(*args, **kwargs)

def list_to_shell_args(args):
    if len(args) == 1:
        return args[0]
    return " ".join([pipes.quote(arg) for arg in args])

def mkdirs(*directories):
    params = list_to_shell_args(directories)
    run("mkdir -p %s" % params)

def setup_directory_structure():
    mkdirs(env.path, env.log_path, env.static_path)

def apt_get_install(*packages):
    params = list_to_shell_args(packages)
    sudo("apt-get install %s" % params)

def pip_install(*packages):
    params = list_to_shell_args(packages)
    run("pip install %s" % params)

@task 
def django_admin(*args):
    params = list_to_shell_args(args)
    with cd(env.path), prefix("pybrew venv use %(venv)s" % env):
        run("PYTHONPATH=. DJANGO_SETTINGS_MODULE=settings django-admin.py %s" % params)

@task
def backup_database():
    django_admin("dumpdata blog --indent 2")

@task
def deploy():
    pass

@task 
def git_clone_repo():
    with cd(env.path):
        run("git clone %(repo)s ." % env)

@task
def git_pull_repo():
    with cd(env.path):
        run("git pull")

@task
def setup():
    apt_get_install("libsqlite3-dev")
    #run("pybrew venv create %(venv)s" % env)
    setup_directory_structure()
    with cd(env.path), prefix("pybrew venv use %(venv)s" % env):
        run("git clone %(repo)s ." % env)
        run("pip install -r %(pip_requirements)s" % env)

# uwsgi -s uwsgi.sock -M -p 1 -w 'django.core.handlers.wsgi:WSGIHandler()' --pythonpath $(pwd) -H $VIRTUAL_ENV --chmod=777

@task
def install_pythonbrew():
    run("curl -kL http://xrl.us/pythonbrewinstall | bash")
    #append("~/.bash_profile", 
    #        "[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc")

@task
def install_python():
    run("pybrew install %(pythonversion)s" % env)

@task
def switch_python(version=env.pythonversion):
    run("pybrew switch %s(pythonversion)s" % env)

@task
def install_uwsgi():
    apt_get_install("libxml2-dev")
    pip_install("uwsgi")

@task
def install_nginx():
    mkdirs("env/build")
    with cd("env/build"):
        run("curl -kL %(nginx_url)s" % env)
        run("tar xzf nginx-*")
        with cd("nginx-*"):
            run("./configure --with-http_ssl_module --prefix=$HOME/env --pid-path=$HOME/env/run/nginx.pid --lock-path=$HOME/env/run/nginx.lock")
            run("make")
            run("make install")

@task
def configure_nginx():
    pass

@task
def start_nginx():
    supervisorctl("start nginx")

@task
def stop_nginx():
    supervisorctl("stop nginx")

@task
def restart_nginx():
    supervisorctl("restart nginx")

@task
def install_supervisord():
    pip_install("supervisord")

@task
def configure_supervisord():
    sudo("ln -sf $HOME/env/conf/supervisord.init.conf /etc/init/supervisord.conf")
    sudo("initctl reload-configuration")

@task
def supervisord_start():
    sudo("start supervisord")

@task
def supervisord_stop():
    sudo("stop supervisord")

@task
def supervisorctl(*args):
    run("supervisorctl %s" % list_to_shell_args(args))

@task
def bootstrap_system():
    install_pythonbrew()
    install_python()
    install_uwsgi()
    install_supervisord()
    install_nginx()

files = {
    "supervisord.conf" : _d("""\
        [unix_http_server]
        file=/tmp/supervisor.sock
        [inet_http_server]
        port=
        username=
        password=
        [supervisord]
        logfile=/home/frozen/env/logs/supervisord.log
        logfile_maxbytes=50MB
        logfile_backups=10
        loglevel=info
        pidfile=/home/frozen/env/run/supervisord.pid
        nodaemon=true
        minfds=1024
        minprocs=200
        [rpcinterface:supervisor]
        supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
        [supervisorctl]
        serverurl=unix:///tmp/supervisor.sock
        history_file=~/.sc_history
        [program:uwsgi-emperor]
        command=uwsgi --emperor "/home/frozen/apps/*.yml"
        [program:nginx]
        command=/home/frozen/env/sbin/nginx
        [fcgi-program:php-fcgi]
        command=/usr/bin/php-cgi -b /tmp/php-fcgi.sock
        socket=unix:///tmp/php-fcgi.sock
        numprocs=5
        process_name=%(program_name)s_%(process_num)02d
        environment=PATH=/usr/bin,PHP_FCGI_MAX_REQUESTS=300
    """),

    "supervisord.sh" : _d("""\
        #!/bin/bash
        source $HOME/.bash_profile
        exec supervisord --nodaemon
    """),
    
    "supervisord.init.conf" : _d("""\
        description  "supervisor"

        start on runlevel [2345]
        stop on runlevel [!2345]
        oom never
        respawn

        exec start-stop-daemon --start -c frozen --exec /home/frozen/env/bin/supervisord.sh
    """),

    "nginx.conf" : _d("""\
        worker_processes    1;
        daemon              off;
        events {
            worker_connections  1024;
        }
        http {
            include             mime.types;
            default_type        application/octet-stream;
            sendfile            on;
            keepalive_timeout   65;
            gzip                on;
            include             /home/frozen/www/nginx.conf;
        }
    """),
}

