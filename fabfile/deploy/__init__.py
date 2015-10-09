# coding: utf-8
import os
import sys

from fabric.contrib import django
from fabric.api import local, lcd
from fabric.tasks import Task

from fab_settings import env

sys.path.append(os.path.dirname(__file__) + '/../../mysite/')

django.settings_module('mysite.settings')

STAGING_BRANCH = 'master'
BASE_PATH = os.path.dirname(__file__) + '/../..'
LOCAL_SETTINGS_PATH = BASE_PATH + '/../settings'


class Staging(Task):
    """
    Deploy project on staging
    """

    def virtualenv(self):
        with lcd(BASE_PATH + '/../'):
            local('source {}/bin/activate'.format(env.venv_name))

    def update_requirements(self):
        with lcd(BASE_PATH):
            local("pip install -r prod_requirements.txt")

    def get_settings(self):
        with lcd(LOCAL_SETTINGS_PATH):
            local('git pull origin master')
            local('cp developer_conf.py ../socraticqs2/mysite/mysite/developer_conf.py')

    def restart_service(self):
        local('sudo supervisorctl restart gunicorn')
        local('sudo supervisorctl restart celery')
        local('sudo service nginx restart')

    def update(self):
        local('git pull origin %s' % STAGING_BRANCH)
        self.get_settings()
        local('find . -name "*.pyc" -print -delete')
        self.virtualenv()
        self.update_requirements()
        with lcd("mysite"):
            local('python manage.py collectstatic --noinput')
            local('python manage.py syncdb --noinput')
        self.restart_service()

    def run(self, suffix=None):
        self.update()


staging = Staging()
