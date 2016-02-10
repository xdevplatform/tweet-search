from __future__ import with_statement

import os
import django

SETTINGS_FILE = "app.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FILE)
django.setup()

PORT = os.environ.get('PORT', 9000)

from fabric.api import *

# run server locally
def start():
    local("python manage.py runserver 127.0.0.1:%s --traceback --settings=%s" % (PORT, SETTINGS_FILE))

# process to invalidate Twitter auth tokens for dormant users
def invalidate():

    OFFBOARD_DAYS = 31
    
    from django.utils import timezone
    from django.contrib.auth.models import User
    from django.db.models import Q
    from social.apps.django_app.default.models import UserSocialAuth
 
    invalidate_delta = timezone.now() - timezone.timedelta(OFFBOARD_DAYS)
    print "Running invalidate process with date: %s" % (invalidate_delta)
     
    # has auth credentials (non-null)
    criteria = Q(extra_data__isnull=False)
    
    # also is past timeframe
    criteria = criteria & (Q(user__last_login__lte=invalidate_delta) | (Q(user__last_login__isnull=True) & Q(user__date_joined__lte=invalidate_delta)))
     
    users = UserSocialAuth.objects.filter(criteria)
    for u in users:
        
        try:
            u.extra_data = None
            u.save()
            print "\tInvalidate user %s (last_login=%s, date_joined=%s)" % (u.user, u.user.last_login, u.user.date_joined)
        except UserSocialAuth.DoesNotExist, e:
            # no record exists; no need to clear anything
            pass
