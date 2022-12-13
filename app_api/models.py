from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from extentions.utils import expriment_result_image_pat
from app_auth.models import User


class DoctorModel(models.Model):
    medical_code = models.BigIntegerField(verbose_name=_('کد نظام پزشکی'))
    skill_title = models.ForeignKey('TitleSkillModel', on_delete=models.CASCADE, verbose_name=_('عنوان تخصص'))
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    units = models.ManyToManyField(to='ExprementModel', verbose_name=_('آزمایشگاه ها'))
    position = models.TextField(max_length=500, null=True, blank=True, verbose_name=_('موقعیت'))
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


class TitleSkillModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('عنوان تخصص'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('عنوان تخصص')
        verbose_name_plural = _('عناوین تخصص‌ها')

    def __str__(self):
        return self.title


class ExprementModel(models.Model):
    CATEGORY_UNITS = (
        ('exprement', _('آزمایشگاه')),
        ('ctscan', _('تصویربرداری-سی تی اسکن')),
        ('radiography_simple', _('تصویربرداری-رادیوگرافی ساده')),
        ('radiography_special', _('تصویربرداری-رادیوگرافی تخصصی')),
        ('mamography', _('تصویربرداری-ماموگرافی')),
        ('sonography', _('تصویربرداری-سونوگرافی')),
    )
    category = models.CharField(max_length=255, choices=CATEGORY_UNITS, verbose_name=_('نوع'))
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    code = models.CharField(max_length=255, verbose_name=_('کد'))
    pos = models.CharField(max_length=255, verbose_name=_('موقعیت'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('بخش')
        verbose_name_plural = _('بخش ها')

    def __str__(self):
        return self.title


class ExprimentResultModel(models.Model):
    TYPE_EX = (
        ('exprement', _('آزمایشگاه')),
        ('ctscan', _('تصویربرداری-سی تی اسکن')),
        ('radiography_simple', _('تصویربرداری-رادیوگرافی ساده')),
        ('radiography_special', _('تصویربرداری-رادیوگرافی تخصصی')),
        ('mamography', _('تصویربرداری-ماموگرافی')),
        ('sonography', _('تصویربرداری-سونوگرافی')),
    )
    type = models.CharField(max_length=20, choices=TYPE_EX, verbose_name=_('نوع نتیجه'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('بیمار'))
    unit = models.ForeignKey(to=ExprementModel, on_delete=models.CASCADE, verbose_name=_('آزمایشگاه'))
    title = models.CharField(max_length=255, verbose_name=_('عنوان آزمایش'))
    result = models.CharField(max_length=255, verbose_name=_('جواب آزمایش'))
    image = models.ImageField(upload_to=expriment_result_image_pat, verbose_name=_('تصویر آزمایش'))
    date = models.DateTimeField(default=timezone.now, verbose_name=_('زمان ثبت نتیجه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نتیجه آزمایش و تصویربرداری')
        verbose_name_plural = _('نتیجه آزمایش ها و تصویربرداری ها')

    def __str__(self):
        return self.code

