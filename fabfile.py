from fabric.api import run, sudo, cd, env

env.use_ssh_config = True
env.warn_only = True

env.roledefs = {
    'apps': ['stacks-app01',]
}

def set_env():
    sudo("source /home/ubuntu/.profile")
    sudo("source /home/ubuntu/stacks/env/bin/activate")

def restart_memcached():
    sudo('pkill memcached')
    sudo('memcached &')

def restart_django():
    set_env()
    with cd("/home/ubuntu/stacks"):
        sudo("pkill manage.py")
        sudo("./manage.py 0.0.0.0 80 &")

def git_pull():
    with cd("/home/ubuntu/stacks"):
        sudo("git pull") # need to add credentials here

def upgrade_app():
    git_pull()
    restart_memcached()
    restart_django()

def rebuild():
    ## !! this method should be deleted once we have real data !!
    set_env()
    run('env')
    run('which python')
    with cd("/home/ubuntu/stacks"):
        sudo("./rebuild.sh") # need to add credentials here

def git_status():
    with cd("/home/ubuntu/stacks"):
        run("git status")