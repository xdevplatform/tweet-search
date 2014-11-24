from __future__ import with_statement

from fabric.api import *
from fabric.contrib import django

SETTINGS_FILE = "app.settings_my"
django.settings_module(SETTINGS_FILE)


# run server locally
def start():
    local("python manage.py runserver 127.0.0.1:9000 --traceback --settings=%s" % SETTINGS_FILE)


