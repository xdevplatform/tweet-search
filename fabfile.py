from __future__ import with_statement

from fabric.api import *
from fabric.contrib import django
import os

SETTINGS_FILE = "app.settings_my"
django.settings_module(SETTINGS_FILE)
PORT = os.environ.get('PORT', 9000)

# run server locally
def start():
    local("python manage.py runserver 127.0.0.1:%s --traceback --settings=%s" % (PORT, SETTINGS_FILE))

