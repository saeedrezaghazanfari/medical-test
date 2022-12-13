from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))
    username = models.CharField(max_length=10, unique=True, verbose_name=_('کدملی'))
    gender = models.CharField(choices=GENDER_USER, default='male', max_length=7, verbose_name=_('جنسیت'))
    age = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('سن'))

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    get_full_name.short_description = _('نام و نام خانوادگی')

    class Meta:
        ordering = ['-id']
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')


