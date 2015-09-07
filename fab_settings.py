"""Settings for Fabric.

Params:

- env.venv_name: name of the current virtualenv
"""
from fabric.api import env


env.venv_name = '.venv'
