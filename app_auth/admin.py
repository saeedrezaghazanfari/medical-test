from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User


class AdminUser(UserAdmin):
    UserAdmin.fieldsets[1][1]['fields'] = (
        'first_name',
        'last_name',
    )
    UserAdmin.fieldsets[2][1]['fields'] = (
        'is_active',
        'is_staff',
        'is_superuser',
        # 'groups',
        # 'user_permissions',
    )
    list_display = ('id', 'username', 'get_full_name')
    ordering = ['-id']

admin.site.register(User, AdminUser)
admin.site.unregister(Group)          # hide groups