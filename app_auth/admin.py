from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DoctorModel, ManagerModel, PatientModel


class AdminUser(UserAdmin):
    UserAdmin.fieldsets[1][1]['fields'] = (
        'first_name',
        'last_name',
        'phone'
    )
    UserAdmin.fieldsets[2][1]['fields'] = (
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
        # 'user_permissions',
    )
    list_display = ('id', 'username', 'get_full_name')
    ordering = ['-id']

admin.site.register(User, AdminUser)
admin.site.register(DoctorModel)
admin.site.register(ManagerModel)
admin.site.register(PatientModel)