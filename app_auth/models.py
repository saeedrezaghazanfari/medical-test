from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(max_length=10, unique=True, verbose_name=_('کدملی'))
    phone = models.CharField(max_length=20, default=0, verbose_name=_('شماره تلفن'))
    permission = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('دسترسی'))

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    get_full_name.short_description = _('نام و نام خانوادگی')

    class Meta:
        ordering = ['-id']
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')


class DoctorModel(models.Model):
    medical_code = models.BigIntegerField(verbose_name=_('کد نظام پزشکی'))
    user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('پزشک')
        verbose_name_plural = _('پزشکان')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    get_full_name.short_description = _('نام پزشک')


class ManagerModel(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('مدیر')
        verbose_name_plural = _('مدیران')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    get_full_name.short_description = _('نام مدیر')


class PatientModel(models.Model):
    username = models.CharField(max_length=10, unique=True, verbose_name=_('کدملی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('بیمار')
        verbose_name_plural = _('بیماران')

    def __str__(self):
        return self.username