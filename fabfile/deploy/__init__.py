# coding: utf-8
import os
import sys

from fabric.contrib import django
from fabric.api import local, run, lcd, cd
from fabric.tasks import Task

from fab_settings import env

sys.path.append(os.path.dirname(__file__) + '/../../mysite/')

django.settings_module('mysite.settings')

STAGING_BRANCH = 'master'
BASE_PATH = os.path.dirname(__file__)

class Deploying(Task):
    """
    Deploy project
    """

    func = local
    func_cd = lcd
    __code_branch = STAGING_BRANCH
    __project_path = os.path.join(BASE_PATH, '/../..')
    __local_settings_path = os.path.join(__project_path, '/../settings')

    def __virtualenv(self):
        with self.func_cd(os.path.join(self.__project_path, '/../')):
            self.func('source {}/bin/activate'.format(env.venv_name))

    def update_requirements(self):
        with self.func_cd(self.__project_path):
            self.func("pip install -r requirements.txt")

    def __get_settings(self, branch='master'):
        with self.func_cd(self.__local_settings_path):
            self.func('git pull origin {0}'.format(branch))
            self.func('cp local_conf_example.py ../socraticqs2/mysite/mysite/local_conf.py')

    def __restart_service(self):
        self.func('sudo supervisorctl restart gunicorn')
        self.func('sudo supervisorctl restart celery')
        self.func('sudo service nginx restart')

    def __update(self):
        self.func('git pull origin %s' % self.__code_branch)
        self.__get_settings()
        self.func('find . -name "*.pyc" -print -delete')
        self.__virtualenv()
        self.update_requirements()
        with self.func_cd("mysite"):
            self.func('python manage.py collectstatic --noinput')
            self.func('python manage.py syncdb --noinput')
        self.__restart_service()

    def run(self, running='local', branch='master', suffix=None):
        if running == 'local':
            self.func = local
            self.func_cd = lcd
        elif running == 'server':
            self.func = run
            self.func_cd = cd

        self.__code_branch = branch
        self.__update()


class Development(Deploying):

    __project_path = os.path.join(BASE_PATH, '/../../dev')
    __code_branch = 'dev'

    def __get_settings(self):
        """On dev staging we don't use prodaction settings"""
        pass


staging = Deploying()
dev = Development()