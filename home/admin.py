from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

UserAdmin.list_display = ('first_name', 'last_name', 'username', 'date_joined', 'is_staff', 'is_superuser')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


