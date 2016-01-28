from __future__ import with_statement

import os
import django

SETTINGS_FILE = "app.settings_my"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FILE)
django.setup()

PORT = os.environ.get('PORT', 9000)

from fabric.api import *

# run server locally
def start():
    local("python manage.py runserver 127.0.0.1:%s --traceback --settings=%s" % (PORT, SETTINGS_FILE))


