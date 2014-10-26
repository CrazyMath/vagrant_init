from __future__ import with_statement
from fabric.api import run, cd
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env


@task()
def install_django():
    """
    Install django.
    """
    run('sudo pip install django')


@task()
def rm_git():
    """
    Remove old repo.
    """
    local('rm -rf .git/')


@task()
def git_init():
    """
    Initial git.
    """
    local('git init')


@task()
def git_add(file_path='.'):
    """
    Command for git add.
    :param file_path:
    """
    local('git add {}'.format(file_path))


@task()
def git_commit(comment=''):
    """
    Add files to git index and commit.
    :param comment:
    """
    local('git commit -m "{}"'.format(comment))


@task()
def update_gitignore():
    """
    Add to gitignore vagrant files and IDE files.
    """
    local("cat .gitignore | sed '$a.vagrant/' > gitignore")
    local("cat gitignore > .gitignore")
    local("cat .gitignore | sed '$a.idea/' > gitignore")
    local("cat gitignore > .gitignore")
    local("rm gitignore")


@task()
def update_fab():
    """
    Replace pattern on project name in fabfile
    """
    local("cat ./fabfile/project.py | sed -e 's/<% {1} %>/{0}/' > project".format(env.project_name, 'project_name'))
    local("cat project > ./fabfile/project.py")
    local("rm project")


@task()
def pre_init():
    """
    Pre init script.
    Remove .gitignore and README.md
    """
    local('rm README.md')
    local('rm .gitignore')


@task()
def post_init():
    """
    Post init script.
    """
    update_fab()
    update_gitignore()
    rm_git()
    git_init()
    git_add()
    git_commit('Initial commit')


@task()
def install_twoscoops(command='icecream'):
    """
    Create project based on twoscoops.
    :param command:
    """
    run('django-admin.py startproject --template=https://github.com/twoscoops/django-twoscoops-project/archive/'
        'master.zip --extension=py,rst,html {} /vagrant'.format(command))


@task()
def requirements():
    """
    Install python requirements.
    """
    run("sudo pip install -r requirements/local.txt")


@task()
def syncdb():
    """
    Run syncdb.
    """
    run("python {}/manage.py syncdb --all --noinput".format(env.project_name))


@task()
def migrate():
    """
    Run migrate.
    """
    run("python {}/manage.py migrate --fake".format(env.project_name))


@task()
def runserver():
    """
    Run dev server.
    """
    run("python {}/manage.py runserver 0.0.0.0:8000".format(env.project_name))


@task()
def filldb():
    """
    Fill db test data.
    """
    run("python {}/manage.py filldb".format(env.project_name))


@task()
def init(project_name=''):
    """
    Init project with param project name.
    :param project_name:
    """
    env.user = 'vagrant'
    env.path = '/vagrant'
    env.project_name = project_name
    with cd(env.path):
        pre_init()
        install_django()
        install_twoscoops(env.project_name)
        requirements()
        syncdb()
        migrate()
        post_init()


@task()
def build():
    """
    Build project.
    """

    env.user = 'vagrant'
    env.path = '/vagrant'
    env.project_name = '<% project_name %>'

    with cd(env.path):
        requirements()
        syncdb()
        migrate()
        filldb()


@task
def update():
    """
    Task for updating project.
    """
    env.user = 'vagrant'
    env.path = '/vagrant'
    env.project_name = '<% project_name %>'

    with cd(env.path):
        requirements()
        syncdb()
        migrate()


@task
def serve():
    """
    Task for start dev server.
    """
    env.user = 'vagrant'
    env.path = '/vagrant'
    env.project_name = '<% project_name %>'

    with cd(env.path):
        runserver()
